$('.datetime_picker').datetimepicker({
    timepicker: false,
    format: 'Y-m-d'
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

function member_show_hide(box, ID, role) {
    if (role == 2) {
        $("#" + box + "_" + ID).toggle("slow");
    }
}

$("#show_sub_menu").click(function() {
    $("#show_sub_menu_ul").slideToggle("slow");
});