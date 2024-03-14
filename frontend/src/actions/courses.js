const addCourse = (course)=>{
    return {
        type: "ADD_COURSE",
        course
    }
}

const clearCourse = ()=>{
    return {
        type: "CLEAR_COURSES"
    }
}
// Getting From Database and Setting in Redux Store

const getAndSetCourses = (filters={},projection={})=>{
    return (dispatch)=>{
        return new Promise((resolve,reject)=>{
            fetch(`${process.env.REACT_APP_API_URL}/get_all_courses`,{
                method: ['POST'],
                body: JSON.stringify({
                    filters,
                    projection
                })
            })
            .then(response => response.json())
            .then(response => {
                dispatch(clearCourse());
                response.allCourses.forEach(course => {
                    dispatch(addCourse(course))
                });
                resolve();
            })
            .catch(error => {
                reject(error);
            })
        })
    }
}

export default getAndSetCourses;