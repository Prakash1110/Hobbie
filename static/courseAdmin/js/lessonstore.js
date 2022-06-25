const url = window.location.href;
var aa = url.split('/')
const pk = aa[aa.length-2];
const origin = window.location.origin;


async function createLesson(data) {
    const formData = new FormData();
    var i;
    for(i=0; i<data.length-1; i++){
        formData.append(data[i].name, data[i].value);
    }
    return fetch(origin + "/admin/course/courseitemstore/lesson/"+ pk + "/", {
        method: 'POST',
        body : formData
    });
}


function validate(e){
    e.preventDefault();    
    createLesson((e.target).elements)
        .then((response) => {
            if(response.redirected){
                window.location = response.url;
            }
        })
    .catch(error => error);
}   

document.getElementById('form').onsubmit = validate;