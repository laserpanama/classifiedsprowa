import asyncio
from playwright.async_api import async_playwright
from app.backend.models.account import Account
from app.backend.models.ad import Ad
from app.backend.services import captcha_service
import logging

logger = logging.getLogger(__name__)

# --- Constants ---
LOGIN_PAGE_URL = "https://www.wanuncios.com/gestionar/"
POST_PAGE_URL = "https://panama.wanuncios.com/publicar/"
LOCAL_CAPTCHA_SOLVER_URL = "https://local-captcha-solver.preview.emergentagent.com/"

# IMPORTANT: These are placeholders and need to be found by inspecting the site's HTML.
LOGIN_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
POST_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"

# --- Helper Functions ---

async def get_captcha_token_with_script(site_key: str, page_url: str) -> str | None:
    """
    Placeholder for solving CAPTCHA with a local script/app.
    This would involve automating the local solver app itself.
    """
    logger.info(f"Attempting to solve CAPTCHA for {page_url} using local script...")
    # This is a placeholder. A real implementation would need to:
    # 1. Launch a new Playwright instance.
    # 2. Navigate to LOCAL_CAPTCHA_SOLVER_URL.
    # 3. Input the site_key and page_url into the solver's form.
    # 4. Click the solve button.
    # 5. Scrape the resulting token from the page.
    logger.warning("Local script-based CAPTCHA solving is a placeholder and will return a dummy token.")
    return "placeholder_token_from_local_script"

async def get_captcha_token(page, method: str, site_key: str, page_url: str, g_recaptcha_response_id: str) -> bool:
    """
    Gets a CAPTCHA token based on the selected method and injects it.
    Returns True on success, False on failure.
    """
    token = None
    if method == 'api':
        logger.info(f"Solving CAPTCHA for {page_url} using 2captcha API...")
        token = await captcha_service.solve_recaptcha_v2(site_key, page_url)
    elif method == 'script':
        token = await get_captcha_token_with_script(site_key, page_url)
    elif method == 'manual':
        logger.warning("Manual CAPTCHA solving selected. The process will pause for 60s. This requires running in non-headless mode and user intervention.")
        await asyncio.sleep(60)
        logger.warning("Manual CAPTCHA solving period has ended.")
        return True # Assume user solved it

    if not token:
        logger.error(f"Could not obtain CAPTCHA token using method '{method}'.")
        return False

    logger.info("CAPTCHA token obtained. Injecting into page.")
    await page.evaluate(f"document.getElementById('{g_recaptcha_response_id}').innerHTML = '{token}';")
    return True

# --- Main Automation Service ---

async def post_ad_to_wanuncios(account: Account, ad: Ad) -> bool:
    """
    Automates the process of posting an ad to wanuncios.com using Playwright.
    """
    # Headless mode is only viable for the 'api' or 'script' methods
    is_headless = account.captcha_solving_method in ['api', 'script']

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=is_headless)
        page = await browser.new_page()

        try:
            # 1. Login
            logger.info(f"Attempting to log in as {account.email} using '{account.captcha_solving_method}' method.")
            await page.goto(LOGIN_PAGE_URL)

            if not await get_captcha_token(page, account.captcha_solving_method, LOGIN_SITE_KEY, LOGIN_PAGE_URL, 'g-recaptcha-response'):
                if account.captcha_solving_method == 'api': # Only fail hard if the API method was chosen
                     raise Exception("Failed to solve login CAPTCHA.")

            await page.fill('input[name="email"]', account.email)
            await page.fill('input[name="password"]', account.wanuncios_password)

            if not is_headless:
                logger.info("Pausing for manual login submission...")
                await asyncio.sleep(10)

            await page.click('button:has-text("Iniciar sesión")')

            try:
                await page.wait_for_url("**/gestionar/mis-anuncios", timeout=15000)
                logger.info("Login successful.")
            except Exception:
                logger.error("Login failed. Check credentials or CAPTCHA token.")
                await page.screenshot(path="login_failed.png")
                await browser.close()
                return False

            # 2. Post Ad
            logger.info("Navigating to ad posting page...")
            await page.goto(POST_PAGE_URL)

            logger.info(f"Filling out form for ad: {ad.title}")
            await page.select_option('select[name="provincia"]', label=ad.province)
            await page.select_option('select[name="categoria"]', label=ad.category)
            await asyncio.sleep(1)
            await page.select_option('select[name="subcategoria"]', label=ad.subcategory)
            await page.fill('input[name="titulo"]', ad.title)
            await page.fill('textarea[name="descripcion"]', ad.description)
            await page.check('input[name="acepto_condiciones"]')

            if not await get_captcha_token(page, account.captcha_solving_method, POST_SITE_KEY, POST_PAGE_URL, 'g-recaptcha-response-1'):
                 if account.captcha_solving_method == 'api':
                    raise Exception("Failed to solve post CAPTCHA.")

            if not is_headless:
                logger.info("Pausing for manual ad submission...")
                await asyncio.sleep(10)

            await page.click('button:has-text("Enviar Anuncio")')

            try:
                await page.wait_for_url("**/anuncio-publicado.html", timeout=20000)
                logger.info("Ad posted successfully!")
            except Exception:
                logger.error("Ad posting may have failed.")
                await page.screenshot(path="ad_posting_failed.png")

            await browser.close()
            return True

        except Exception as e:
            logger.error(f"An error occurred during automation: {e}")
            await page.screenshot(path="automation_error.png")
            await browser.close()
            return False
