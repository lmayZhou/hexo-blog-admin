/*! jQuery Validation Plugin - v1.13.1 - 10/14/2014
 * http://jqueryvalidation.org/
 * Copyright (c) 2014 Jörn Zaefferer; Licensed MIT */
! function (a) {
    "function" == typeof define && define.amd ? define(["jquery", "jquery.validate.min"], a) : a(jQuery)
}(function ($) {
    var icon = "<i class='fa fa-times-circle'></i> ";
    $.extend($.validator.messages, {
        required: icon + "This field is required.",
        remote: icon + "Please fix this field.",
        email: icon + "Please enter a valid email address.",
        url: icon + "Please enter a valid URL.",
        date: icon + "Please enter a valid date.",
        dateISO: icon + "Please enter a valid date ( ISO ).",
        number: icon + "Please enter a valid number.",
        digits: icon + "Please enter only digits.",
        creditcard: icon + "Please enter a valid credit card number.",
        equalTo: icon + "Please enter the same value again.",
        maxlength: $.validator.format(icon + "Please enter no more than {0} characters." ),
        minlength: $.validator.format(icon + "Please enter at least {0} characters." ),
        rangelength: $.validator.format(icon + "Please enter a value between {0} and {1} characters long." ),
        range: $.validator.format(icon + "Please enter a value between {0} and {1}." ),
        max: $.validator.format(icon + "Please enter a value less than or equal to {0}." ),
        min: $.validator.format(icon + "Please enter a value greater than or equal to {0}." )
    });
});