import React from 'react';
import PropTypes from 'prop-types';
import Typography from '@material-ui/core/Typography';
// https://github.com/mui-org/material-ui/blob/master/docs/src/pages/getting-started/templates/dashboard/Title.js
export default function Title(props) {
  return (
    <Typography component="h2" variant="h6" color="primary" gutterBottom>
      {props.children}
    </Typography>
  );
}

Title.propTypes = {
  children: PropTypes.node,
};