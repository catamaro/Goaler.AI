$(document).ready(function () {
    $('.plans_content').hide()
    $('.plan_content').hide()

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
        console.log($(this).attr('id'))
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
