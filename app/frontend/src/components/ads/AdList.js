import React from 'react';
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
  TableCaption,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';

const AdList = ({ ads, onEdit, onDelete, onPublish }) => {
  if (!ads || ads.length === 0) {
    return <p>No ads found. Create one to get started!</p>;
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableCaption>A list of your saved ads.</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>Title</TableHead>
            <TableHead>Category</TableHead>
            <TableHead>Last Published</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {ads.map((ad) => (
            <TableRow key={ad.id}>
              <TableCell className="font-medium">{ad.title}</TableCell>
              <TableCell>{ad.category} / {ad.subcategory}</TableCell>
              <TableCell>{ad.last_published_at ? new Date(ad.last_published_at).toLocaleString() : 'Never'}</TableCell>
              <TableCell className="text-right">
                <Button variant="secondary" size="sm" onClick={() => onPublish(ad.id)}>
                  Publish
                </Button>
                <Button variant="outline" size="sm" className="ml-2" onClick={() => onEdit(ad)}>
                  Edit
                </Button>
                <Button variant="destructive" size="sm" className="ml-2" onClick={() => onDelete(ad.id)}>
                  Delete
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default AdList;
