import React from 'react';
import './_teacherComponent.scss';

const TeacherComponent = (props)=>{
    const { username, name, department, courseAssigned } = props;
    return(
        <div className="teacherMainDiv">
            <div className="teacherMainContainer">
                <div className="teacherData">
                    <header>
                        <h2>
                            {name}<span>({username})</span>
                        </h2>

                    </header>
                    <div className="teacherBody">
                    <p>Courses assigned : </p>
                            <ul style={{ paddingLeft: '40px' }}>
                                {courseAssigned?.map((course, index) => (
                                    <li key={index}>{course}</li>
                                ))}
                            </ul>
                        <p>
                            Department : <span>{department}</span>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default TeacherComponent;