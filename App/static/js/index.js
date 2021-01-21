
function changeFormTypes() {
    $('#end_hour').clone().attr('type','time').insertAfter('#end_hour').prev().remove();
    $('#start_hour').clone().attr('type','time').insertAfter('#start_hour').prev().remove();
    $('#date').clone().attr('type','date').insertAfter('#date').prev().remove();
    $('#start_date').clone().attr('type','date').insertAfter('#start_date').prev().remove();
    $('#end_date').clone().attr('type','date').insertAfter('#end_date').prev().remove();
    $('#deadline').clone().attr('type','date').insertAfter('#deadline').prev().remove();
    $('#birthday').clone().attr('type','date').insertAfter('#birthday').prev().remove();
    $('#email').clone().attr('type','email').insertAfter('#email').prev().remove();
}

$(document).ready(function () {
    $('.plans_content').hide()
    $('.plan_content').hide()

    changeFormTypes()

    $(".plans_button_down").click(function () {
        var content = $(this).closest(".plans_header").parent().children().eq(1)
        if(content.is(":visible")){
            content.fadeOut('fast');
        }
        else{
            content.fadeIn('fast');
        } 
    })

    $(".plans_option_btn").click(function () {
        var id = "plan_option" + $(this).attr('id')
        plan_content = $("#" + id)

        if(plan_content.is(":visible")){
            plan_content.fadeOut('fast');
        }
        else{
            plan_content.parent().children().hide()
            plan_content.fadeIn('fast');
        } 
    })
});
