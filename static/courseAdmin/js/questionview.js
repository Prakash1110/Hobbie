const token = (document.getElementsByName('csrfmiddlewaretoken')[0]).value;
const origin = window.location.origin;
// var aa = url.split('/');

async function deleteQuestion(pk, csrftoken) {  
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrftoken);
    return fetch(origin + "/admin/course/courseitem/quiz/questions/del/"+pk+"/", {
        method: 'POST',
        body : formData
    }).then(response => response.json());
}


delbtn = document.getElementsByClassName('delete-question');

var arr = Array.prototype.slice.call( delbtn );

arr.forEach(element => {
    element.addEventListener('click', ()=>{
        deleteQuestion((element.id).split("-")[1], token)
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

async function editQuestion(pk, csrftoken, label, num) {  
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrftoken);
    formData.append('label', label);
    formData.append('number', num);

    // formData.append(data);
    return fetch(origin + "/admin/course/courseitem/quiz/questions/edit/"+pk+"/", {
        method: 'POST',
        body : formData
    }).then(response => response.json());
}




editBtn = document.getElementsByClassName('edit-question');
var editArr = Array.prototype.slice.call( editBtn );


editArr.forEach(element => {
    element.addEventListener('click', ()=>{
        let quesId = (element.id).split("-")[1];
        let questionNum = document.getElementById('question-num '+ quesId);
        let questionLabel = document.getElementById('question '+ quesId);
        let questionDel = document.getElementById('del-'+quesId);
        let questionEdit = document.getElementById('edit-'+quesId);
        let inputQuestionNum = document.createElement('input');
        
        inputQuestionNum.type = "number";
        inputQuestionNum.value = parseInt(questionNum.innerHTML);
        
        let inputQuestionLabel = document.createElement('input');
        let editDone = document.createElement('button');
        
        editDone.innerHTML = "DONE";
        editDone.id = quesId;
        inputQuestionLabel.value = questionLabel.innerHTML;

        questionLabel.parentNode.removeChild(questionEdit);
        questionLabel.parentNode.replaceChild(editDone, questionDel);
        questionNum.parentNode.replaceChild(inputQuestionNum, questionNum);
        questionLabel.parentNode.replaceChild(inputQuestionLabel, questionLabel);

        editDone.addEventListener('click', ()=>{

            label = inputQuestionLabel.value;
            num = inputQuestionNum.value;

            editQuestion(quesId, token, label, num)
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
});


async function editChoice(pk, csrftoken, text, isCorrect) {  
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrftoken);
    formData.append('text', text);
    formData.append('is_correct', isCorrect);

    // formData.append(data);
    return fetch(origin + "/admin/course/courseitem/quiz/choices/edit/"+pk+"/", {
        method: 'POST',
        body : formData
    }).then(response => response.json());
}



choiceEditBtn = document.getElementsByClassName('edit-choice');
var choiceEditBtnArr = Array.prototype.slice.call( choiceEditBtn );


choiceEditBtnArr.forEach(element => {
    element.addEventListener('click', ()=>{
        let chId = (element.id).split("-")[1];
        let choice = document.getElementById('choice-'+chId);
        let choiceInput = document.createElement('input');
        let isCorP = document.createElement('span');
        let isCorLab = document.createTextNode("IsCorrect");
        let isCorrect = document.createElement('input');
        isCorrect.type = "checkbox";
        isCorrect.value = 1; 
        isCorrect.style = "-webkit-appearance: auto;";
        isCorP.appendChild(isCorrect);
        isCorP.appendChild(isCorLab);
        isCorP.style = "font-size : 20px;position:absolute; left:50%";
        choiceInput.value = choice.innerHTML;   
        choice.parentNode.appendChild(isCorP);
        choice.parentNode.replaceChild(choiceInput, choice);

        let choiceDone = document.createElement('button');

        choiceDone.innerHTML = "DONE";
        choiceDone.style = "font-size : 10px;position:absolute; left:90%"
        element.parentNode.replaceChild(choiceDone, element);
        
        choiceDone.addEventListener('click', ()=>{

            console.log(choiceInput.value);
            console.log(isCorrect.checked);     
            text = choiceInput.value;
            is_correct = isCorrect.checked;
            console.log(isCorrect);
            editChoice(chId, token, text, is_correct)
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
});