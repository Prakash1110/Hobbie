const url = window.location.href;
var aa = url.split('/')
const pk = aa[aa.length-2];
const origin = window.location.origin;

async function createQuiz(data) {
    const formData = new FormData();
    var i;
    for(i=0; i<data.length-1; i++){
        formData.append(data[i].name, data[i].value);
    }
    return fetch(origin + "/admin/course/courseitemstore/quiz/"+ pk + "/", {
        method: 'POST',
        body : formData
    }).then(response => response);
}



function validate(e){
    e.preventDefault();    
    createQuiz((e.target).elements)
        .then((response) => {
            console.log(response);
            if(response.redirected){
                // call question creation
                window.location = response.url;
            }
        })
        .catch(error => error);
}   

document.getElementById('form').onsubmit = validate;


q = document.getElementById('add-ques');

q.addEventListener("click", function(){
    console.log('clicked');
    var target_id = "questions-form";
        str = `
                <div class="question-form">
                    <div class="mb-3">
                        <label for="question-num" class="form-label">Question Number</label>
                        <input type="number" name='question-num' class="form-control">
                    </div>
                    <div class="mb-3">
                        <label for="question-description" class="form-label">Question</label>
                        <input type="text" name='question-description' class="form-control">
                    </div>
                    <div class="choices row">
                        <div class="mb-3 col-3">
                            <label for="option-1" class="form-label">Option 1</label>
                            <input type="text" name='option-1' class="form-control">
                        </div>
                        <div class="mb-3 col-3">
                            <label for="option-2" class="form-label">Option 2</label>
                            <input type="text" name='option-2' class="form-control">
                        </div>
                        <div class="mb-3 col-3">
                            <label for="option-3" class="form-label">Option 3</label>
                            <input type="text" name='option-3' class="form-control">
                        </div>
                        <div class="mb-3 col-3">
                            <label for="option-4" class="form-label">Option 4</label>
                            <input type="text" name='option-4' class="form-control">
                        </div>
                    </div>
                </div>

                <div class="correct-choice row my-3">
                        <div class="col12">
                            Correct option is...
                        </div>
                        <select class="form-select" name="correct-choice" aria-label="Default select example">
                            <option value="a" selected>Option A</option>
                            <option value="b">Option B</option>
                            <option value="c">Option C</option>
                            <option value="d">Option D</option>
                        </select>
                    </div>
        `
        $('#questions-form').append(str);
})