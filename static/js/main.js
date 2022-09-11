"use strict";


let app = {

    loader: '',
    alertErrorMessage: 'Произошла ошибка. Пожалуйста повторите еще раз!',
    geoMap: null,
    needResize: false,
    currentVersion: 'PC',
    init: function init() {
        app.resizeWindowEvent();
    },

    resizeWindowEvent: function resizeWindowEvent() {
        let headerNav = document.querySelector('.header__nav'),
            headerFeedback = document.querySelector('.header__feedback-btn');

        if (window.innerWidth > 991 && app.currentVersion !== "PC") {
            app.currentVersion = 'PC';
            app.needResize = true;
        }

        if (window.innerWidth <= 991 && window.innerWidth > 767 && app.currentVersion !== "TABLET") {
            app.currentVersion = 'TABLET';
            app.needResize = true;
        }

        if (window.innerWidth <= 767 && app.currentVersion !== "MOBILE") {
            app.currentVersion = 'MOBILE';
            app.needResize = true;
        }

        if (app.needResize) {
            if (app.currentVersion === "PC") {

            }

            if (app.currentVersion === "TABLET" || app.currentVersion === "PC") {


            }

            if (app.currentVersion === "TABLET" || app.currentVersion === "MOBILE") {
                if (headerNav) {
                    document.querySelector('.mobile-menu__container').append(headerNav);
                    document.querySelector('.mobile-menu__container').append(headerFeedback);
                }
            }

            if (app.currentVersion === "MOBILE") {

            }

            app.needResize = false;
        }
    },


};

window.onload = () => {
    app.init();

    window.addEventListener('resize', function () {
        app.resizeWindowEvent();
    });


    document.querySelector('.mobile-menu-btn').addEventListener('click', (e) => {


        document.querySelector('.mobile-menu').classList.toggle('opened');
        document.querySelector('.mobile-menu-btn').classList.toggle('opened');
        document.querySelector('header').classList.toggle('mobile-menu-opened');
        document.querySelector('body').classList.toggle('mobile-menu-opened');


        e.preventDefault();
    });

    document.querySelectorAll('.mobile-menu__container .header__nav-category > a').forEach(function (link) {
        link.addEventListener('click', (e) => {

            link.classList.toggle("opened");

            e.preventDefault();
        });
    });

    document.querySelectorAll('.header__nav .list-title').forEach(function (link) {
        link.addEventListener('click', (e) => {

            link.parentNode.classList.toggle("opened");

            e.preventDefault();
        });
    });

    document.querySelectorAll('.attributes__title').forEach(function (link) {
        link.addEventListener('click', (e) => {

            document.querySelectorAll('.attributes__title').forEach(function (check) {
                check.classList.remove("checked");
            });

            document.querySelectorAll('.attributes__content-block').forEach(function (tabContent) {
                tabContent.classList.remove("showed");
            });

            document.querySelector('.attributes__content-block[data-tab="' + link.dataset.tab + '"]').classList.add("showed")

            link.classList.add("checked");


            e.preventDefault();
        });
    });







    document.querySelectorAll('.default-select select').forEach(function (select) {

        let options = document.createElement('div');
        options.classList.add('select-options');

        select.querySelectorAll('option').forEach(function (option) {
            let newOption =  document.createElement('div');
            newOption.setAttribute('value', option.getAttribute('value'));
            newOption.innerText = option.innerText;

            if (option.getAttribute('disabled') !== null) {
                newOption.classList.add('disabled');
            }

            options.append(newOption);

            newOption.addEventListener('click', (e) => {

                if (newOption.classList.contains('disabled')) {
                    return false;
                }

                select.parentNode.classList.remove('opened');
                select.value = newOption.getAttribute('value');
            });
        });

        select.parentNode.append(options);

        select.addEventListener('mousedown', (e) => {

            let selectBox = e.target.parentNode;

            selectBox.classList.toggle('opened')

            e.preventDefault();
        });
    });





    const sliders = document.querySelectorAll('input[type="range"]');

    if (sliders.length > 0) {
        sliders[0].addEventListener('input', (e) => {
            if(+sliders[0].value > +sliders[1].value){
                sliders[1].value = +sliders[0].value;
            }
        });

        sliders[1].addEventListener('input', (e) => {
            if(+sliders[1].value < +sliders[0].value){
                sliders[0].value = +sliders[1].value;
            }
        });

        sliders.forEach((slider) => {
            slider.addEventListener('change', () => {
                console.log(`from ${sliders[0].value} to ${sliders[1].value}`);
            })
        });
    }

};
