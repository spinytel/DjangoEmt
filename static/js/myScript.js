$(document).ready(function(){
    $('.datetime_picker').datetimepicker({
      timepicker:false,
      format:'Y-m-d'
    });
      // Filter Design - Start
    var table_height = $('.ticket_table').height();
    //alert(table_height);
    $("#table_filter_upper").css("height",table_height+27);
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
