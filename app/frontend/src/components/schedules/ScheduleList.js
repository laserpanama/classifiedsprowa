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
import { Switch } from '@/components/ui/switch';

const ScheduleList = ({ schedules, onEdit, onDelete, onToggle }) => {
  if (!schedules || schedules.length === 0) {
    return <p>No schedules found. Create one to get started!</p>;
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableCaption>A list of your ad republishing schedules.</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>Ad ID</TableHead>
            <TableHead>Interval (hours)</TableHead>
            <TableHead>Next Run</TableHead>
            <TableHead>Active</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {schedules.map((schedule) => (
            <TableRow key={schedule.id}>
              <TableCell className="font-mono text-xs">{schedule.ad_id.slice(0, 8)}...</TableCell>
              <TableCell>{schedule.republish_interval_hours}</TableCell>
              <TableCell>{new Date(schedule.next_republish_at).toLocaleString()}</TableCell>
              <TableCell>
                <Switch
                  checked={schedule.is_active}
                  onCheckedChange={(checked) => onToggle(schedule.id, { is_active: checked })}
                />
              </TableCell>
              <TableCell className="text-right">
                <Button variant="outline" size="sm" onClick={() => onEdit(schedule)}>
                  Edit
                </Button>
                <Button variant="destructive" size="sm" className="ml-2" onClick={() => onDelete(schedule.id)}>
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

export default ScheduleList;
