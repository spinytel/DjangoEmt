//Pop up Div Declaration - Start
$(document).ready(function() {
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

  $(".entry,#closeEntry").click( function () {
      var id = $(this).find('input[name="user_id"]').val();
      ajax_entry_userID(id);
      $('#popUpEntry input[name="passing_user_id"]').val(id);
      popup('popUpEntry')
  });


  $(".leave,#closeLeave").click( function () {
      var id = $(this).find('input[name="user_id"]').val();
      ajax_leave_userID(id);
      $('#popUpLeave input[name="passing_user_id"]').val(id);
      popup('popUpLeave')
  });


  $(".att_entry,#closeEntry_details").click( function () {
      var id = $(this).find('input[name="user_id"]').val();
      var date = $(this).find('input[name="date"]').val();
      ajax_att_popup(date);
      $('#popUpEntry_details input[name="passing_user_id"]').val(id);
      $('#popUpEntry_details input[name="passing_date"]').val(date);
      popup('popUpEntry_details')
  });


  $(".att_leave,#closeLeave_details").click( function () {
      var user_id = $(this).find('input[name="user_id"]').val();
      var att_id = $(this).find('input[name="att_id"]').val();
      var date = $(this).find('input[name="date"]').val();
      ajax_att_popup(date);
      $('#popUpLeave_details input[name="passing_user_id"]').val(user_id);
      $('#popUpLeave_details input[name="passing_date"]').val(date);
      $('#popUpLeave_details input[name="passing_ID"]').val(att_id);
      popup('popUpLeave_details')
  });



  $(".task_limit_add,#close_task_limit").click( function () {
      popup('task_limit_add');
  });

  $(".task_limit_edit,#close_task_limit_edit").click( function () {
      var edit_id = $(this).find('input[name="edit_id"]').val();
      ajax_limit_edit(edit_id);
      $('#task_limit_edit input[name="passing_user_id"]').val(edit_id);
      popup('task_limit_edit');
  });

  $(".task_add_edit,#close_task_add_edit").click( function () {
      var task_id = $(this).find('input[name="task_id"]').val();
      ajax_task_add_edit(task_id);
      $('#task_add_edit input[name="passing_task_id"]').val(task_id);
      popup('task_add_edit');
  });

jQuery('.dp_milestone_start_date').datetimepicker({
    timepicker: false,
    format: 'Y-m-d'
});

jQuery('.dp_milestone_due_date').datetimepicker({
    timepicker: false,
    format: 'Y-m-d'
});

$("#add_another_i").click(function () {
    $("#add_files").append('<input style="margin: 5px 5px 2px 5px;" type="file" name="project_file">');
});
//Pop up Div Declaration - End
var previous_id ;
function project_menu_toggle(ID){
    if(previous_id == null){
        $('#p_menu_'+ID).toggle();

        if($('#p_menu_'+ID).css("display") == "block"){
            $('#p_click_'+ID).addClass('active_menu_button');
        }else{
            $('#p_click_'+ID).removeClass('active_menu_button');
        }
    }else if(previous_id != ID){
        $('#p_menu_'+previous_id).hide();
        $('#p_click_'+previous_id).removeClass('active_menu_button');

        $('#p_menu_'+ID).show();
        $('#p_click_'+ID).addClass('active_menu_button');
    }else{
        $('#p_menu_'+ID).toggle();

        if($('#p_menu_'+ID).css("display") == "block"){
            $('#p_click_'+ID).addClass('active_menu_button');
        }else{
            $('#p_click_'+ID).removeClass('active_menu_button');
        }
    }
    previous_id = ID;
}



function member_show_hide(box, ID, role) {
    if (role == 2) {
        $("#" + box + "_" + ID).toggle("slow");
    }
}

$("#show_sub_menu").click(function() {
    $("#show_sub_menu_ul").slideToggle("slow");
});
