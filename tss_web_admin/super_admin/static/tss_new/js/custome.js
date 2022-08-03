$(document).ready(function()  {
    $('#sidebar-menu > ul > li > a').click(function () {
        /*   $(this).parent().addClass('sidebar_nav_actv');*/
        /*  $(this).parent().siblings().removeClass('sidebar_nav_actv');*/
        $(this).siblings('.sidebar_sub_division').toggleClass('wdth', 4000);
        $(this).parent().siblings().find('.sidebar_sub_division').removeClass('wdth', 4000);
        if($('.sidebar_sub_division').hasClass('wdth')) {
            $('.content-page').addClass('clpsedcntnt', 4000);
            $('.TimetrackerFooter').addClass('TimetrackerFooter_Open', 4000);
        }
        else {
            $('.content-page').removeClass('clpsedcntnt', 4000);
            $('.TimetrackerFooter').removeClass('TimetrackerFooter_Open', 4000);
        }
    });
    $('p.splnav').click(function () {
        $(this).parent().addClass('sidebar_nav_actv');
        $(this).parent().siblings().removeClass('sidebar_nav_actv');
        $(this).siblings('.sidebar_sub_division').toggleClass('wdth', 4000);
        $(this).parent().siblings().find('.sidebar_sub_division').removeClass('wdth', 4000);
        if($('.sidebar_sub_division').hasClass('wdth')) {
            $('.content-page').addClass('clpsedcntnt', 4000)
        }
        else {
            $('.content-page').removeClass('clpsedcntnt', 4000)
        }
    });
    $('.bootm_toggle_button').click(function () {
        $(".sidebar_sub_division").removeClass('wdth', 4000);
        $('.content-page').removeClass('clpsedcntnt', 4000);
    });
    $('.sidebar_sub_division a').click(function () {
        $("this").addClass('sidebar_nav_sub_actv');
        $(".sidebar_nav_actv").removeClass('sidebar_nav_actv');
    });
    $(".sidebar_sub_division li a").each(function () {
        window.location.href, $(this).prop("href") == window.location.href && ($(this).closest('.sidebar_sub_division').addClass("wdth", 4000)
        )
        if($('.sidebar_sub_division').hasClass('wdth')) {
            $('.content-page').addClass('clpsedcntnt', 4000)
        }
        else {
            $('.content-page').removeClass('clpsedcntnt', 4000)
        }
    });
    $(".sidebar_sub_division a").each(function () {
        window.location.href, $(this).prop("href") == window.location.href && ($(this).addClass("current"),
            $(this).closest('li.active').addClass("sidebar_nav_actv"),
            $(this).parent().parent().parent().parent().addClass("sidebar_nav_actv"),
            $(this).closest('.sidebar_sub_division').parent().addClass("sidebar_nav_actv"))
    });
    $("#sidebar-menu > ul > li > a").each(function () {
        window.location.href, $(this).prop("href") == window.location.href && $(this).parent().addClass("sidebar_nav_actv");
    });
    $(".submnu > li > a").each(function () {
        window.location.href, $(this).prop("href") == window.location.href && $(this).parent().parent().addClass("show");
    });
    $(".submnu_sub > li > a").each(function () {
        window.location.href, $(this).prop("href") == window.location.href && $(this).parent().parent().addClass("show");
        $(this).parent().parent().siblings(".crnt").addClass("show shobg")
    });
    $(".nav_second_sub > li.crnt > a").click(function () {
        $(this).parent().siblings().removeClass("show")
// $(this).attr('aria-expanded') === "false")
    });
// *************************************************************
    $(".bootm_toggle_settings_button .submnu li a").each(function () {
        /*  alert("afdhgh")*/
        window.location.href, $(this).prop("href") == window.location.href && ($(this).addClass("current"),
            $(this).closest('li.active').addClass("sidebar_nav_actv"),
            $(this).closest('li.active').addClass("sidebar_nav_actv"),
            $(this).closest('.bootm_toggle_settings_button').addClass("sidebar_nav_actv"))
    });
    $("#sidebar-menu > ul > li > a").each(function () {
        window.location.href, $(this).prop("href") == window.location.href && $(this).parent().addClass("sidebar_nav_actv");
    });
    $(".submnu > li > a").each(function () {
        window.location.href, $(this).prop("href") == window.location.href && $(this).parent().parent().addClass("show");
    });
// *************************************************************
    $('#searchform').submit(function (e) {
        e.preventDefault(); // stop form submission
    });
    $('.open-right').click(function () {
        $('.sidenav').toggleClass('sidenavshow');
    });
    $(".enlarge").click(function () {
        $(this).parent().parent().parent().parent().parent().addClass("largclss");
    });
    $(".dslarge").click(function () {
        $(this).parent().parent().parent().parent().parent().removeClass("largclss");
    });
    $(".enlarge_modal").click(function () {
        $(this).parent().parent().parent().parent().addClass("largclss");
    });
    $(".dslarge_modal").click(function () {
        $(this).parent().parent().parent().parent().removeClass("largclss");
    })
});
$(window).scroll(function() {
    var scroll = $(window).scrollTop();
    if (scroll >= 0) {
        $("#wrapper").addClass("modal-open2");
    }
});
// *************************************************************
let ready = $(document).ready(function () {
    function checkForInput(element) {
        const $label = $(element).siblings('label.inputText');
        if ($(element).val().length > 0) {
            $label.addClass('input-has-value');
        } else {
            $label.removeClass('input-has-value');
        }
    }
    $('input.input').each(function () {
        checkForInput(this);
    });
    $('input.input').on('change keyup', function () {
        checkForInput(this);
    });
    function checkForTextarea(element) {
        const $label = $(element).siblings('label.inputText');
        if ($(element).val().length > 0) {
            $label.addClass('input-has-value');
        } else {
            $label.removeClass('input-has-value');
        }
    }
    $('textarea.input_textaerea').each(function () {
        checkForTextarea(this);
    });
    $('textarea.input_textaerea').on('change keyup', function () {
        checkForTextarea(this);
    });
    $('.input').each(function () {
        if ($(this).hasClass('getVal')) {
            $(this).siblings('label.inputText').addClass('input-has-value');
        }
    });
    $('select').on('change', function () {
        var selectVal = $("select option:selected").val();
        $(this).siblings('label.inputText').addClass('input-has-value');
    });
    $(".clearbtnn").click(function () {
        $('label.inputText').removeClass('input-has-value ');
    });
});
