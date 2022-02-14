import * as React from 'react';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import LinkUI from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './Title';

// Generate Row Data
function createData(id, date, value) {
  return { id, date, value };
}

export default function RecentKeys() {

  const [pairs, setPairs] = useState([])

  useEffect(() => {
    fetch("/recentKeys").then(
      res => res.json()
    ).then(
      data => {
        var temp = []
        for (let i = 0; i < data.date.length; i++) {
          temp.push(createData(i, data.date[i], data.value[i]))
        }
        setPairs(temp)
        console.log(temp)
      }
    )
  }, [])

  return (
    <React.Fragment>
      <Title>Recent Keys</Title>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Date</TableCell>
            <TableCell>Key Value</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {pairs.map((pair) => (
            <TableRow key={pair.id}>
              <TableCell>{pair.date}</TableCell>
              <TableCell>{pair.value}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <LinkUI color="primary" sx={{ mt: 3 }}>
        <Link to="/gallery">See more keys</Link>
      </LinkUI>
    </React.Fragment>
  );
}
