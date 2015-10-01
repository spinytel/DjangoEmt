toastr.options.positionClass = 'toast-bottom-right';
toastr.options.extendedTimeOut = 0; //1000;
toastr.options.timeOut = 8000;
toastr.options.fadeOut = 250;
toastr.options.fadeIn = 250;
toastr.options.closeButton = true;
toastr.options.closeHtml = '<button><i class="fa fa-close"></i></button>';
toastr.options.progressBar = true;
toastr.options.preventDuplicates = true;

$(document).ready(function(){
    $('.datetime_picker').datetimepicker({
      timepicker:false,
      format:'Y-m-d'
    });
      // Filter Design - Start
    $('#filter_button').on({
        'click': function(){
            if($('#table_filter_inner').css("display") == "block"){
                $('.filter_arrow').attr('src','/static/img/right_arrow.png');
                $("#table_filter_inner").css("display","none");
                $("#table_filter").css("width","2%");
                $("#table_data").css("width","98%");
                $("#table_filter_upper").css("height",$('.ticket_table').height()+27);
            }else{
                $('.filter_arrow').attr('src','/static/img/left_arrow.png');
                $("#table_filter_inner").css("display","block");
                $("#table_filter").css("width","20%");
                $("#table_data").css("width","80%");
                $("#table_filter_upper").css("height","inherit");
            }
        }
    });
    $("#add_another_i").click(function(){
      $("#add_files").append('<input style="margin: 5px 5px 2px 5px;" type="file" name="project_file">');
    });

    $("#add_another_if").click(function(){
      $("#add_files").append('<input style="margin: 5px 5px 2px 5px;" type="file" name="ticket_file">');
    });

    $("#add_another_if1").click(function(){
      $("#add_files").append('<input style="margin: 5px 5px 2px 5px;" type="file" name="ticket_file">');
    });


    jQuery('.dp_milestone_start_date').datetimepicker({
        timepicker: false,
        format: 'Y-m-d'
    });

    jQuery('.dp_milestone_due_date').datetimepicker({
        timepicker: false,
        format: 'Y-m-d'
    });
    //Pop up Div Declaration - End

    function member_show_hide(box, ID, role) {
        if (role == 2) {
            $("#" + box + "_" + ID).toggle("slow");
        }
    }
    $("#show_sub_menu").click(function() {
        $("#show_sub_menu_ul").slideToggle("slow");
    });



});

//Deleting Existing Project File
function delete_p_file(ID, file_name, project){
    var loader    = $('.loader');
    var url = $('#delete_url').val();
    var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
    var isYes=confirm('Do you really want to delete this File ?');
    if(ID && isYes && file_name){
        $.ajax({
            cache: false,
            type: "POST",
            url: url,
            data: { ID: ID, f_name: file_name,csrfmiddlewaretoken: csrfmiddlewaretoken,project:project},
            beforeSend: function () {
                loader.show();
            },
            success: function(data) {
                if(data == 1){
                    $("#e_p_f_"+ID).hide();
                }else{
                    alert('Something wrong, Please try again.')
                }
            },
            complete: function () {
                loader.hide();
            }
        });
    }
}
