const token = (document.getElementsByName('csrfmiddlewaretoken')[0]).value;
const origin = window.location.origin;
async function deleteCourse(couseSlug, csrftoken){
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrftoken);
    return fetch(origin + '/admin/course/coursechange/'+ couseSlug + '/', {
        method: 'POST',
        body : formData
    }).then(response => response.json())
};



delbtn = document.getElementsByClassName('delete-course');

var arr = Array.prototype.slice.call( delbtn )
arr.forEach(element => {
    element.addEventListener('click', ()=>{
        deleteCourse(element.id, token)
            .then((json) => {
                if(json.status===200){
                    alert(json.message);
                    location.reload();
                }else if(json.status === 405){
                    alert(json.message);
                }else{
                    alert("server not responding. Please try after some time");
                }
            })
            .catch(error => error);
    });
});
