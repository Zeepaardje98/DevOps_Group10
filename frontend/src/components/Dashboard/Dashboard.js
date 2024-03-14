import { connect } from 'react-redux';
import React , { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { getUsernameFromCookie } from '../../helperFunction/getCookie';

import './_dashboard.scss';

class Dashboard extends Component{

  render(){
    const logginStatus = !!getUsernameFromCookie();

    if(logginStatus){
      return(
          <div className="dashboard-container">
              <h1>Welcome to the One-Click Attendance App</h1>
              <p className="dashboard-description">Dashboard</p>
              <div className="user-info">
                  <h2 className="username">{this.props.username}</h2>
                  <p className="user-role">{this.props.role}</p>
              </div>
          </div>
      )
    } else {
        return <Redirect to="/login"/>
    }
  }
}

const mapStateToProps = (state) => {
    return {
        username: state.user.username,
        role: state.user.role
    }
}

export default connect(mapStateToProps)(Dashboard);
