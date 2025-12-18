import requests
import asyncio
import os
import logging

logger = logging.getLogger(__name__)

async def solve_recaptcha_v2(site_key: str, page_url: str) -> str | None:
    """
    Solves a reCAPTCHA v2 using 2captcha.com.

    :param site_key: The reCAPTCHA site key from the target page.
    :param page_url: The URL of the page with the reCAPTCHA.
    :return: The g-recaptcha-response token, or None if failed.
    """
    api_key = os.getenv("TWOCAPTCHA_API_KEY")
    if not api_key:
        logger.error("TWOCAPTCHA_API_KEY not found in environment variables.")
        return None

    # 1. Submit the CAPTCHA for solving
    submit_url = "http://2captcha.com/in.php"
    params = {
        "key": api_key,
        "method": "userrecaptcha",
        "googlekey": site_key,
        "pageurl": page_url,
        "json": 1
    }
    try:
        response = requests.post(submit_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != 1:
            logger.error(f"2Captcha submission failed: {data.get('request')}")
            return None
        request_id = data.get("request")
        logger.info(f"CAPTCHA submitted successfully. Request ID: {request_id}")
    except requests.RequestException as e:
        logger.error(f"Error submitting CAPTCHA to 2captcha: {e}")
        return None

    # 2. Poll for the result
    result_url = "http://2captcha.com/res.php"
    params = {
        "key": api_key,
        "action": "get",
        "id": request_id,
        "json": 1
    }
    for _ in range(24):  # Poll for up to 120 seconds (24 * 5s)
        await asyncio.sleep(5)
        try:
            response = requests.get(result_url, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == 1:
                logger.info("CAPTCHA solved successfully.")
                return data.get("request")
            elif data.get("request") == "CAPCHA_NOT_READY":
                logger.info("CAPTCHA not ready, polling again...")
            else:
                logger.error(f"Failed to solve CAPTCHA: {data.get('request')}")
                return None
        except requests.RequestException as e:
            logger.error(f"Error polling for CAPTCHA result: {e}")
            return None

    logger.error("CAPTCHA solving timed out.")
    return None
