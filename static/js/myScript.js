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
    timepicker:false,
    format:'Y-m-d'
});

jQuery('.dp_milestone_due_date').datetimepicker({
    timepicker:false,
    format:'Y-m-d'
});

    $(".public_holiday_add,#close_public_holiday_add").click( function () {
        popup('public_holiday_add');
    });

    $(".public_holiday_edit,#close_public_holiday_edit").click( function () {
        var holiday_ID = $(this).find('input[name="holiday_ID"]').val();
        ajax_holiday_edit_load(holiday_ID);
        $('#public_holiday_edit input[name="holiday_ID"]').val(holiday_ID);
        popup('public_holiday_edit');
    });


    $(".entry_time_add,#close_entry_time").click( function () {
        popup('entry_time_add');
    });

    $(".entry_time_edit,#close_entry_time_edit").click( function () {
        var entry_ID = $(this).find('input[name="entry_ID"]').val();
        ajax_entry_edit_load(entry_ID);
        $('#entry_time_edit input[name="passing_user_ID"]').val(entry_ID);
        popup('entry_time_edit');
    });

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


//Pop Up All Method - Start
function toggle(div_id) {
    var el = document.getElementById(div_id);
    if ( el.style.display == 'none' ) {	el.style.display = 'block';}
    else {el.style.display = 'none';}
}
function blanket_size(popUpDivVar) {
    if (typeof window.innerWidth != 'undefined') {
        viewportheight = window.innerHeight;
    } else {
        viewportheight = document.documentElement.clientHeight;
    }
    if ((viewportheight > document.body.parentNode.scrollHeight) && (viewportheight > document.body.parentNode.clientHeight)) {
        blanket_height = viewportheight;
    } else {
        if (document.body.parentNode.clientHeight > document.body.parentNode.scrollHeight) {
            blanket_height = document.body.parentNode.clientHeight;
        } else {
            blanket_height = document.body.parentNode.scrollHeight;
        }
    }
    var blanket = document.getElementById('blanket');
    blanket.style.height = blanket_height + 'px';
    var popUpDiv = document.getElementById(popUpDivVar);
    popUpDiv_height=blanket_height/2-200;//200 is half popup's height
    //popUpDiv.style.top = popUpDiv_height + 'px';
    popUpDiv.style.top = '140px';
}
function window_pos(popUpDivVar) {
    if (typeof window.innerWidth != 'undefined') {
        viewportwidth = window.innerHeight;
    } else {
        viewportwidth = document.documentElement.clientHeight;
    }
    if ((viewportwidth > document.body.parentNode.scrollWidth) && (viewportwidth > document.body.parentNode.clientWidth)) {
        window_width = viewportwidth;
    } else {
        if (document.body.parentNode.clientWidth > document.body.parentNode.scrollWidth) {
            window_width = document.body.parentNode.clientWidth;
        } else {
            window_width = document.body.parentNode.scrollWidth;
        }
    }
    var popUpDiv = document.getElementById(popUpDivVar);
    window_width=window_width/2-200;//200 is half popup's width
    popUpDiv.style.left = window_width + 'px';
}
function ajax_entry_userID(id){
    if(id){
        $.ajax({
            cache: false,
            type: "POST",
            url: "attendance_ajax_userID.php",
            data: { ID: id},
            success: function(data) {
                $(".entry_ajax").html(data);
            }
        });
    }
}
function entry_data_save(page_name){
    var entry_userID = $('#entry_userID').val();
    var entry_time = $('input[name="entry_time"]').val();
    var entry_id = ('entry_'+entry_userID);
    var leave_id = ('leave_'+entry_userID);
    if(entry_userID && entry_time){
        $.ajax({
            cache: false,
            type: "POST",
            url: "attendance_ajax_save_entry.php",
            data: { userID: entry_userID, time: entry_time},
            success: function(data) {
                if(data == 1){
                    document.getElementById("blanket").style.display="none";
                    document.getElementById("popUpEntry").style.display="none";
                    /*
                    document.getElementById(entry_id).innerHTML ="<span class='entry_na'>N/A</span>";
                    document.getElementById(leave_id).innerHTML ='<a class="leave"><input type="hidden" name="user_id" value="'+ entry_userID +'"/><span class="leave_time">Exit</span></a>';
                    */
                    alert('Entry Time Added Successfully !!!');
                    location.href = page_name;
                    //$('#'+table_id).html(data);
                }else if(data == 0){
                    alert('Something Wrong !!! Try Again.');
                }
            }
        });
    }else{
        if(!entry_userID){
            alert('Ajax not Working !!! Try Again.')
        }else if(!entry_time){
            alert('Entry time is Mandatory')
        }
    }
}
function ajax_leave_userID(id){
    if(id){
        $.ajax({
            cache: false,
            type: "POST",
            url: "attendance_ajax_userID.php",
            data: { ID: id},
            success: function(data) {
                $(".leave_ajax").html(data);
            }
        });
    }
}
function leave_data_save(page_name){
    var leave_userID = $('#leave_userID').val();
    var leave_time = $('input[name="leave_time"]').val();
    var entry_id = ('entry_'+leave_userID);
    var leave_id = ('leave_'+leave_userID);
    if(leave_userID && leave_time){
        $.ajax({
            cache: false,
            type: "POST",
            url: "attendance_ajax_save_leave.php",
            data: { userID: leave_userID, time: leave_time},
            success: function(data) {
                if(data != 0){
                    document.getElementById("blanket").style.display="none";
                    document.getElementById("popUpLeave").style.display="none";
                    if(page_name == 'home.php'){
                        document.getElementById(leave_id).innerHTML ="<div class='att_content_red' style='margin-bottom: 5px;'>Exit : <span class='att_content_time'>"+data+"</span></div>";
                    }else{
                        document.getElementById(leave_id).innerHTML ="<span class='leave_na'>N/A</span>";
                    }
                    //$('#'+table_id).html(data);
                }else if(data == 0){
                    alert('Something Wrong !!! Try Again.')
                }
            }
        });
    }else{
        if(!leave_userID){
            alert('Ajax not Working !!! Try Again.')
        }else if(!leave_time){
            alert('Leave time is Mandatory')
        }
    }
}

function ajax_att_popup(date){
    if(date){
        $.ajax({
            cache: false,
            type: "POST",
            url: "attendance_att_ajax_date.php",
            data: { date: date},
            success: function(data) {
                $(".entry_ajax").html(data);
            }
        });
    }
}
function popup(windowname) {
    blanket_size(windowname);
    window_pos(windowname);
    toggle('blanket');
    toggle(windowname);
}
//Pop Up All Method - End


//Roster Schedule All Method - Start
function roster_s(id){
    var roster_id = id;
    var roster_group_ID = $('input[name="roster_group_ID_'+roster_id+'"]').val();
    var roster_date    = $('input[name="roster_date_'+roster_id+'"]').val();
    var roster_duty    = $('select[name="duty_'+roster_id+'"]').val();
    if(roster_group_ID && roster_date && roster_duty && roster_id){
        $.ajax({
            cache: false,
            type: "POST",
            url: "roster_ajax_add.php",
            data: { rgID: roster_group_ID, rDate: roster_date, rDuty: roster_duty, i: roster_id },
            beforeSend: function () {
                loader.show();
            },
            success: function(data) {
                $("#roster_"+roster_id+"").html(data);
            },
            complete: function () {
                loader.hide();
            }
        });
    }else{
        if(!roster_group_ID || !roster_date || !roster_duty || !roster_id){
            alert('Javascript not Working !!! Try Again.')
        }
    }
}
function roster_update(id){
    var roster_id = id;
    var rosterID = $('input[name="roster_ID_'+roster_id+'"]').val();
    if(rosterID && roster_id){
        $.ajax({
            cache: false,
            type: "POST",
            url: "roster_ajax_edit.php",
            data: { rID: rosterID, id: roster_id },
            beforeSend: function () {
                loader.show();
            },
            success: function(data) {
                $("#roster_"+roster_id+"").html(data);
            },
            complete: function () {
                loader.hide();
            }
        });
    }else{
        if(!rosterID || !roster_id){
            alert('Javascript not Working !!! Try Again.')
        }
    }
}
function roster_u(id){
    var roster_id = id;
    var roster_group_ID = $('input[name="roster_group_ID_'+roster_id+'"]').val();
    var rosterID       = $('input[name="roster_ID_'+roster_id+'"]').val();
    var roster_duty    = $('select[name="duty_'+roster_id+'"]').val();
    if(rosterID && roster_duty && roster_group_ID && roster_id){
        $.ajax({
            cache: false,
            type: "POST",
            url: "roster_ajax_update.php",
            data: { rID: rosterID, rgID: roster_group_ID , rDuty: roster_duty, i: roster_id },
            beforeSend: function () {
                loader.show();
            },
            success: function(data) {
                $("#roster_"+roster_id+"").html(data);
            },
            complete: function () {
                loader.hide();
            }
        });
    }else{
        if(!rosterID || !roster_duty || !roster_group_ID || roster_id){
            alert('Javascript not Working !!! Try Again.')
        }
    }
}
//Roster Schedule All Method - End

function entry_task_add_save(){
    var user_ID = $('select[name="user_ID"]').val();
    var task_date = $('input[name="task_date"]').val();
    var task_limit = $('input[name="task_limit"]').val();
    if(user_ID && task_date && task_limit){
        $.ajax({
            cache: false,
            type: "POST",
            url: "task_limit_ajax_add.php",
            data: { userID: user_ID, taskDate: task_date, taskLimit: task_limit },
            success: function(data) {
                if(data == 1){
                    document.getElementById("blanket").style.display="none";
                    document.getElementById("task_limit_add").style.display="none";
                    alert('Task Limit Added Successfully !!!');
                    location.href='task_limit.php';
                }else{
                    alert('Something Wrong !!! Try Again.')
                }
            }
        });
    }else{
        if(!user_ID){
            alert('Employee Selection is Mandatory')
        }else if(!task_date){
            alert('Date is Mandatory')
        }else if(!task_limit){
            alert('Task Limit is Mandatory')
        }
    }
}
function ajax_limit_edit(id){
    if(id){
        $.ajax({
            cache: false,
            type: "POST",
            url: "task_limit_edit_ajax_load.php",
            data: { ID: id},
            success: function(data) {
                $(".limit_ajax").html(data);
            }
        });
    }
}
function entry_task_edit_save(){
    var user_ID = $('input[name="passing_user_id"]').val();
    var task_ID = $('select[name="task_ID"]').val();
    if(user_ID && task_ID){
        $.ajax({
            cache: false,
            type: "POST",
            url: "task_limit_edit_ajax.php",
            data: { userID: user_ID, taskID: task_ID},
            success: function(data) {
                if(data == 1){
                    document.getElementById("blanket").style.display="none";
                    document.getElementById("task_limit_edit").style.display="none";
                    alert('Default Task Limit Updated Successfully !!!');
                    location.href='task_limit.php';
                }else{
                    alert('Something Wrong !!! Try Again.');
                }
            }
        });
    }else{
        if(!user_ID){
            alert('Javascript not Working !!! Try Again.');
        }else if(!task_ID){
            alert('Task Limit Selection is Mandatory');
        }
    }
}

function ajax_task_add_edit(task_ID){
    if(task_ID){
        $.ajax({
            cache: false,
            type: "POST",
            url: "task_add_edit_ajax_load.php",
            data: {taskID: task_ID},
            success: function(data) {
                $(".limit_ajax").html(data);
            }
        });
    }
}
function update_task(){
    var task_id = $('input[name="passing_task_id"]').val();
    var task    = $('textarea[name="task"]').val();
    if(task_id && task){
        $.ajax({
            cache: false,
            type: "POST",
            url: "task_add_edit_ajax.php",
            data: { taskID: task_id, task: task},
            success: function(data) {
                if(data == 1){
                    document.getElementById("blanket").style.display="none";
                    document.getElementById("task_add_edit").style.display="none";
                    alert('Task Updated Successfully !!!');
                    location.href='task_add.php';
                }else{
                    alert('Something Wrong !!! Try Again.');
                }
            }
        });
    }else{
        if(!task_id){
            alert('Javascript not Working !!! Try Again.');
        }else if(!task){
            alert('Task is Mandatory');
        }
    }
}
function entry_task_add(){
    var task    = $('textarea[name="task_new"]').val();
    if(task){
        $.ajax({
            cache: false,
            type: "POST",
            url: "task_add_ajax.php",
            data: { task: task},
            success: function(data) {
                if(data == 1){
                    alert('Task Added Successfully !!!');
                    location.href='task_add.php';
                }else{
                    alert('Something Wrong !!! Try Again.');
                }
            }
        });
    }else{
        if(!task){
            alert('Task is Mandatory');
        }
    }
}
// Task Functions - End

function entry_time_save(){
    var user_ID = $('select[name="user_ID"]').val();
    var entry_date = $('input[name="entry_date"]').val();
    if(user_ID && entry_date){
        $.ajax({
            cache: false,
            type: "POST",
            url: "entry_time_ajax_add.php",
            data: { userID: user_ID, entryDate: entry_date},
            success: function(data) {
                if(data == 1){
                    document.getElementById("blanket").style.display="none";
                    document.getElementById("entry_time_add").style.display="none";
                    alert('Entry Time Added Successfully !!!');
                    location.href='entry_time.php';
                }else{
                    alert('Something Wrong !!! Try Again.')
                }
            }
        });
    }else{
        if(!user_ID){
            alert('Employee Selection is Mandatory')
        }else if(!entry_date){
            alert('Effective Date & Time is Mandatory')
        }
    }
}
function ajax_entry_edit_load(id){
    if(id){
        $.ajax({
            cache: false,
            type: "POST",
            url: "entry_time_ajax_edit_load.php",
            data: { ID: id},
            success: function(data) {
                $(".entry_ajax").html(data);
            }
        });
    }
}
function entry_time_edit_save(){
    var user_ID = $('input[name="passing_user_ID"]').val();
    var time_ID = $('select[name="time_ID"]').val();
    if(user_ID && time_ID){
        $.ajax({
            cache: false,
            type: "POST",
            url: "entry_time_ajax_edit.php",
            data: { userID: user_ID, timeID: time_ID},
            success: function(data) {
                if(data == 1){
                    document.getElementById("blanket").style.display="none";
                    document.getElementById("entry_time_edit").style.display="none";
                    alert('Default Entry Time Updated Successfully !!!');
                    location.href='entry_time.php';
                }else{
                    alert('Something Wrong !!! Try Again.');
                }
            }
        });
    }else{
        if(!user_ID){
            alert('Javascript not Working !!! Try Again.');
        }else if(!time_ID){
            alert('Entry Time Selection is Mandatory');
        }
    }
}
// Entry Time Functions - End

function public_holiday_save(){
    var holiday_date = $('input[name="holiday_date"]').val();
    var holiday_name = $('input[name="holiday_name"]').val();
    var holiday_note = $('textarea[name="holiday_note"]').val();
    if(holiday_date && holiday_name){
        $.ajax({
            cache: false,
            type: "POST",
            url: "public_holiday_ajax_add.php",
            data: { holidayDate: holiday_date, holidayName: holiday_name, holidayNote: holiday_note},
            success: function(data) {
                if(data == 1){
                    document.getElementById("blanket").style.display="none";
                    document.getElementById("public_holiday_add").style.display="none";
                    alert('Public Holiday Added Successfully !!!');
                    location.href='public_holiday.php';
                }else{
                    alert('Something Wrong !!! Try Again.')
                }
            }
        });
    }else{
        if(!holiday_date){
            alert('Date is Mandatory')
        }else if(!holiday_name){
            alert('Name of Holiday is Mandatory')
        }
    }
}
function ajax_holiday_edit_load(id){
    if(id){
        $.ajax({
            cache: false,
            type: "POST",
            url: "public_holiday_ajax_load.php",
            data: { ID: id},
            success: function(data) {
                $(".holiday_ajax").html(data);
            }
        });
    }
}
function public_holiday_edit_save(){
    var holiday_ID   = $('input[name="holiday_ID"]').val();
    var holiday_date = $('input[name="e_holiday_date"]').val();
    var holiday_name = $('input[name="e_holiday_name"]').val();
    var holiday_note = $('textarea[name="e_holiday_note"]').val();
    if(holiday_ID && holiday_date && holiday_name){
        $.ajax({
            cache: false,
            type: "POST",
            url: "public_holiday_ajax_edit.php",
            data: { holidayID: holiday_ID, holidayDate: holiday_date, holidayName: holiday_name, holidayNote: holiday_note},
            success: function(data) {
                if(data == 1){
                    document.getElementById("blanket").style.display="none";
                    document.getElementById("public_holiday_edit").style.display="none";
                    alert('Public Holiday Updated Successfully !!!');
                    location.href='public_holiday.php';
                }else{
                    alert('Something Wrong !!! Try Again.');
                }
            }
        });
    }else{
        if(!holiday_ID){
            alert('Javascript not Working !!! Try Again.');
        }else if(!holiday_date){
            alert('Date is Mandatory');
        }else if(!holiday_name){
            alert('Name of Holiday is Mandatory');
        }
    }
}

function how_load(id){
    if(id == 11){
        var url = '11'
    }else if(id == 12){
        var url = '12'
    }else if(id == 13){
        var url = '13'
    }else if(id == 21){
        var url = '21'
    }else if(id == 22){
        var url = '22'
    }else if(id == 31){
        var url = '31'
    }else if(id == 32){
        var url = '32'
    }
    if(id){
        $.ajax({
            cache: false,
            type: "POST",
            url: "howTo/"+url+".php",
            data: { ID: id},
            beforeSend: function () {
                loader.show();
            },
            success: function(data) {
                $( ".onePage-nav li a" ).removeClass("active_howTo");
                $( "#"+id+" a" ).addClass("active_howTo");
                $('.howTo-details').hide().html(data).fadeIn('slow');
            },
            complete: function () {
                loader.hide();
            }
        });
    }
}
// Public Holiday Functions - End



//Attendance Edit Functions - Start
function f_edit_entry(ID,div_id){
    $.ajax({
        cache: false,
        type: "POST",
        url: "attendance_edit_entry.php",
        data: { ID: ID, divId: div_id},
        beforeSend: function () {
            loader.show();
        },
        success: function(data) {
            if(data == 0){
                alert('Something Wrong, Try again');
            }else{
                $("#edit_entry_"+div_id).html(data);
            }
        },
        complete: function () {
            loader.hide();
        }
    });
}
function f_edit_entry_save(ID,div_id){
    var att_time   = $('input[name="edit_entry_time_'+ID+'"]').val();
    $.ajax({
        cache: false,
        type: "POST",
        url: "attendance_edit_entry_save.php",
        data: { ID: ID, attTime: att_time, divId: div_id},
        beforeSend: function () {
            loader.show();
        },
        success: function(data) {
            if(data == 0){
                alert('Something Wrong, Try again');
            }else if(data == 1){
                alert('Time Format is Wrong, Try again');
            }else{
                $("#edit_entry_"+div_id).html(data);
            }
        },
        complete: function () {
            loader.hide();
        }
    });
}
function f_edit_leave(ID,div_id){
    $.ajax({
        cache: false,
        type: "POST",
        url: "attendance_edit_leave.php",
        data: { ID: ID, divId: div_id},
        beforeSend: function () {
            loader.show();
        },
        success: function(data) {
            if(data == 0){
                alert('Something Wrong, Try again');
            }else{
                $("#edit_leave_"+div_id).html(data);
            }
        },
        complete: function () {
            loader.hide();
        }
    });
}
function f_edit_leave_save(ID,div_id){
    var att_time   = $('input[name="edit_leave_time_'+ID+'"]').val();
    $.ajax({
        cache: false,
        type: "POST",
        url: "attendance_edit_leave_save.php",
        data: { ID: ID, attTime: att_time, divId: div_id},
        beforeSend: function () {
            loader.show();
        },
        success: function(data) {
            if(data == 0){
                alert('Something Wrong, Try again');
            }else if(data == 1){
                alert('Time Format is Wrong, Try again');
            }else{
                $("#edit_leave_"+div_id).html(data);
            }
        },
        complete: function () {
            loader.hide();
        }
    });
}
function toggle_entry_leave(div_id, date, user_ID, date_type){
    if(date_type == "normal"){
        $.ajax({
            cache: false,
            type: "POST",
            url: "attendance_edit_normal_toggle.php",
            data: { dateI: date, userID: user_ID, dateType: date_type, divId: div_id},
            beforeSend: function () {
                loader.show();
            },
            success: function(data) {
                if(data == 0){
                    alert('Something Wrong, Try again');
                }else{
                    $("#off_entry_"+div_id).html(data);
                }
            },
            complete: function () {
                loader.hide();
            }
        });
    }else if(date_type == "weekly"){
        $.ajax({
            cache: false,
            type: "POST",
            url: "attendance_edit_weekly_toggle.php",
            data: { dateI: date, userID: user_ID, dateType: date_type, divId: div_id},
            beforeSend: function () {
                loader.show();
            },
            success: function(data) {
                if(data == 0){
                    alert('Something Wrong, Try again');
                }else{
                    $("#on_entry_"+div_id).html(data);
                }
            },
            complete: function () {
                loader.hide();
            }
        });
    }else if(date_type == "public"){
        $.ajax({
            cache: false,
            type: "POST",
            url: "attendance_edit_public_toggle.php",
            data: { dateI: date, userID: user_ID, dateType: date_type, divId: div_id},
            beforeSend: function () {
                loader.show();
            },
            success: function(data) {
                if(data == 0){
                    alert('Something Wrong, Try again');
                }else{
                    $("#on_entry_"+div_id).html(data);
                }
            },
            complete: function () {
                loader.hide();
            }
        });
    }
}
function reset(date, user_ID, date_type){
    $.ajax({
        cache: false,
        type: "POST",
        url: "attendance_edit_reset.php",
        data: { dateI: date, userID: user_ID, dateType: date_type},
        beforeSend: function () {
            loader.show();
        },
        success: function(data) {
            if(data == 0){
                alert('Something Wrong, Try again');
            }else{
                $("#myTable").html(data);
            }
        },
        complete: function () {
            loader.hide();
        }
    });
}
//Attendance Edit Functions - End



//Leave Request Functions - Start
function leave_yes(ID){
    $.ajax({
        cache: false,
        type: "POST",
        url: "l_schedule_manager_yes.php",
        data: { iD: ID},
        beforeSend: function () {
            loader.show();
        },
        success: function(data) {
            if(data == 0){
                alert('Something Wrong, Try again');
            }else{
                $("#leave_status_"+ID+"").html(data);
            }
        },
        complete: function () {
            loader.hide();
        }
    });
}

function leave_no(ID){
    $.ajax({
        cache: false,
        type: "POST",
        url: "l_schedule_manager_no.php",
        data: { iD: ID},
        beforeSend: function () {
            loader.show();
        },
        success: function(data) {
            if(data == 0){
                alert('Something Wrong, Try again');
            }else{
                $("#leave_status_"+ID+"").html(data);
            }
        },
        complete: function () {
            loader.hide();
        }
    });
}
//Leave Request Functions - End



//Project Related Functions - Start
function member_show_hide(box,ID,role){
    if(role == 2){
        $("#"+box+"_"+ID).toggle("slow");
    }
}

//Deleting Existing Project File
function delete_p_file(ID, project_ID, file_name){
    var isYes=confirm('Do you really want to delete this File ?');
    if(ID && isYes && project_ID && file_name){
        $.ajax({
            cache: false,
            type: "POST",
            url: "project_file_delete.php",
            data: { ID: ID, p_ID: project_ID, f_name: file_name},
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

//Deleting Existing Ticket File
function delete_t_file(ID, creator_ID, file_name){
    var isYes=confirm('Do you really want to delete this File ?');
    if(ID && isYes && creator_ID && file_name){
        $.ajax({
            cache: false,
            type: "POST",
            url: "project_ticket_file_delete.php",
            data: { ID: ID, c_ID: creator_ID, f_name: file_name},
            beforeSend: function () {
                loader.show();
            },
            success: function(data) {
                if(data == 1){
                    $("#e_t_f_"+ID).hide();
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
//Project Related Functions - End


//Add Roster Group - Start
function add_roster_group(value){
    if(value == 'roster'){
        $.ajax({
            cache: false,
            type: "POST",
            url: "user_roster_group.php",
            success: function(data) {
                $("#AddRosterGroup").html(data);
            }
        });
    }else{
        $("#AddRosterGroup").html('');
    }
}
//Add Roster Group - End
