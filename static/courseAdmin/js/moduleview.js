const token = (document.getElementsByName('csrfmiddlewaretoken')[0]).value;
const url = window.location.href;
// var aa = url.split('/');

async function deleteModule(pk, csrftoken) {
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrftoken);
    return fetch(url + pk + '/', {
        method: 'POST',
        body : formData
    }).then(response => response.json());
}


delbtn = document.getElementsByClassName('delete-module');

var arr = Array.prototype.slice.call( delbtn )
arr.forEach(element => {
    element.addEventListener('click', ()=>{
        deleteModule(element.id, token)
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
