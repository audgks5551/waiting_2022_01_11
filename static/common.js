console.log("common.js 로딩됨");
 // storeType
function storeType__check(number) {
        if ($(`input[id='id_store_type_${number}']`).prop('checked')) {
            $(`label[for='id_store_type_${number}']`).addClass("active");
        } else {
            $(`label[for='id_store_type_${number}']`).removeClass("active");
        }
}
function storeType__init(number) {
    $(`input[id='id_store_type_${number}']`).click(function() {
        storeType__check(number);
    });
}

// amenity
function amenity__check(number) {
    if ($(`input[id='id_amenities_${number}']`).prop('checked')) {
        $(`label[for='id_amenities_${number}']`).addClass("active");
    } else {
        $(`label[for='id_amenities_${number}']`).removeClass("active");
    }
}


function amenity__init(number) {
    $(`input[id='id_amenities_${number}']`).click(function () {
        amenity__check(number);
    });
}

// theme
function theme__check(number) {
    if ($(`input[id='id_themes_${number}']`).prop('checked')) {
        $(`label[for='id_themes_${number}']`).addClass("active");
    } else {
        $(`label[for='id_themes_${number}']`).removeClass("active");
    }
}

function theme__init(number) {
    $(`input[id='id_themes_${number}']`).click(function () {
        theme__check(number);
    });
}

// taste
function taste__check(number) {
    if ($(`input[id='id_tastes_${number}']`).prop('checked')) {
        $(`label[for='id_tastes_${number}']`).addClass("active");
    } else {
        $(`label[for='id_tastes_${number}']`).removeClass("active");
    }
}

function taste__init(number) {
    $(`input[id='id_tastes_${number}']`).click(function () {
        taste__check(number);
    });
}


