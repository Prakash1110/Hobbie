// THIS JS FILE IS FOR TESTING PURPOSE ONLY
 


console.log('working');
// add event 
lesson = document.getElementById('add-lesson');
$("#add-lesson").click(function(e){
    str = `
    <hr>
    <div class="lesson-form">
                <h4>Lesson Form</h4>
                <div class="mb-3">
                    <label for="course-item-num-lesson" class="form-label">Course item number</label>
                    <input type="number" name='course-item-num-lesson' class="form-control" >
                </div>
                <div class="mb-3">
                    <label for="lesson-title" class="form-label">Lesson Title</label>
                    <input type="text" name='lesson-title' class="form-control" id="lesson-title">
                </div>
                <div class="mb-3">
                    <label for="lesson-duration" class="form-label">Lesson Duration</label>
                    <input type="number" name='lesson-duration' class="form-control" id="lesson-duration">
                </div>
                <div class="mb-3">
                    <label for="lesson-url" class="form-label">Lesson Url</label>
                    <input type="text" name='lesson-url' class="form-control" id="lesson-url">
                </div>
            </div>
    `
    $('#submit').before(str);
});
var quiz = 0;
$('#add-quiz').click(function(){
    quiz = quiz + 1;
    str = `
    <div class="quiz-form my-3">
        <hr>
        <h4>Quiz Form</h4>
        <div class="mb-3">
            <label for="course-item-num-quiz" class="form-label">Course item number</label>
            <input type="number" name='course-item-num-quiz' class="form-control">
        </div>
        <div class="mb-3">
            <label for="quiz-title" class="form-label">Quiz Title</label>
            <input type="text" name='quiz-title' class="form-control">
        </div>
        <div class="mb-3">
            <label for="question-count" class="form-label">Question count</label>
            <input type="number" name='question-count' class="form-control">
        </div>
        <div class="mb-3">
            <label for="quiz-description" class="form-label">Quiz Description</label>
            <input type="text" name='quiz-description' class="form-control">
        </div>
        <div id='add-questions-quiz-${quiz}' class="btn btn-success add-ques">ADD QUESTIONS</div>
        <hr>
    </div>
    `
    $('#submit').before(str);
})

q = document.getElementById('main-form');
q.addEventListener("click", function(e){
    classes = e.target.className;
    if(classes === 'btn btn-success add-ques')
    {
        var target_id = e.target.id;
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
        $(`#${target_id}`).before(str);
    }
})


