"use strict";

function like() {
    var like = $(this);
    var type = like.data('type');
    var pk = like.data('pk');
    $.ajax({
        url: "/" + type + "/" + pk + "/like",
        type: "POST",

        success: function (json) {
            like.css("color", json.color);
            like.next().css("color", "black");
            like.prev()[0].textContent = json.rate;
        }
    });

    return false;

}

function dislike() {
    var dislike = $(this);
    var type = dislike.data("type");
    var pk = dislike.data("pk");
    $.ajax({
        url: "/" + type + "/" + pk + "/dislike",
        type: "POST",

        success: function (json) {
            dislike.css("color", json.color);
            dislike.prev().css("color", "black");
            dislike.prev().prev()[0].textContent = json.rate;
        }
    });

    return false;

}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(function () {
    $.ajaxSetup({
        headers: {"X-CSRFToken": getCookie("csrftoken")}
    });
});


$(function () {
    $(".fa-plus").click(like);
    $(".fa-minus").click(dislike);
});


$(function () {
    $.each($(".fa"), function (ind, item) {
        var type = $(item).data("type");
        var pk = $(item).data("pk");
        $.ajax({
            url: "/" + type + "/" + pk + "/isliked",
            type: "POST",

            success: function (json) {
                if ($(item).hasClass("fa-plus") && json.isliked === 1) {
                    $(item).css("color", "green");
                }
                if ($(item).hasClass("fa-minus") && json.isliked === -1) {
                    $(item).css("color", "red");
                }
            }
        })
    });
});
