export const setDepartment = (name) => ({
    type: 'SET_DEPARTMENT',
    department: {
        name
    }
})


export const getAndSetDepartments = () => {
    return (dispatch) => {
        return new Promise((resolve, reject)=>{
            fetch(`${process.env.REACT_APP_API_URL}/get_all_departments`,{
                method: 'POST'
            })
            .then(response => response.json())
            .then(response => {
                // console.log("RESPONSE : ",response)
                response.allDepartments.forEach(department => {
                    dispatch(setDepartment(department.name))
                });

                resolve();
            })
            .catch((error)=>{
                reject(error);
            })
        })
    }
}