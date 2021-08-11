$("input#take_input_text").keyup(() => {
    var name = $("input#take_input_text").val()
    var url = "/AdminModel/get_users_name/"
    var userid;
    var username;
    var date_created;
    if (name.length > 2) {
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'name': name
            })
        }).then((response) => {
            return response.json()
        }).then((data) => {
            $(".add_data").empty()

            for (var i = 0; i < data.data.length; i++) {
                userid = data.data[i].id
                username = data.data[i].name
                date_created = data.data[i].date_created
                str_ = '<div class="arrange__users__by__grid">\
                                <p> ' + userid + ' </p>\
                                <p> ' + username + ' </p>\
                                <p>  ' + date_created + '   </p >\
                                <p><a href="">Details</a></p>\
                            </div><br>'
                $(".add_data").append(str_)
            }
        })
    } else if (name.length == 0) {
        location.reload()
    }
})


$("input#take__orders__input").keyup(() => {
    var id = $("input#take__orders__input").val()
    var url = "/AdminModel/get_orders/"

    if (id.length > 5) {
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'id': id
            })
        }).then((response) => {
            return response.json()
        }).then((data) => {
            $(".orders__apppend").empty();
            $(".chnge_to_prson").text("Customer")
            for (var i = 0; i < data.data.cc.product.length; i++) {
                $(".orders__apppend").append(
                    '<div class="arrange__users__by__grid orders__informations">\
                        <p>' + data.data.cc.product[i][0] + '<span style=color:red;> x' + data.data.cc.product[i][1] + '</span></p>\
                        <p>' + data.data.cc.date_ordered + '</p>\
                        <p>' + data.data.cc.date_deliverd + '</p>\
                        <p>' + data.data.cc.customer + '</p>\
                    </div> <br>'
                )
            }
        })
    } else if (id.length == 0) {
        location.reload()
    }
})


$("a.deliverd_orders").click(() => {
    url = "/AdminModel/get_deliverd_or_pending/"
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'status': true
        })
    }).then((response) => {
        return response.json()
    }).then((data) => {
        $(".orders__apppend").empty();
        for (var i = 0; i < data.data.length; i++) {
            for (var j = 0; j < data.data[i].product.length; j++){
                $(".orders__apppend").append(
                    '<div class="arrange__users__by__grid orders__informations">\
                        <p>' + data.data[i].product[j][0] + '<span style=color:red;> x' + data.data[i].product[0][1] + '</span></p>\
                        <p>' + data.data[i].date_ordered + '</p>\
                        <p>' + data.data[i].date_deliverd + '</p>\
                        <p class = "some_need_ful_info">' + data.data[i].transaction_id + '</p>\
                    </div> <br>'
                )
            }
            
        }
        itsucks()
    })
})

$("a.pending_orders").click(() => {
    url = "/AdminModel/get_deliverd_or_pending/"
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'status': false
        })
    }).then((response) => {
        return response.json()
    }).then((data) => {
        $(".orders__apppend").empty();
        for (var i = 0; i < data.data.length; i++) {
            for (var j = 0; j < data.data[i].product.length; j++) {
                $(".orders__apppend").append(
                    '<div class="arrange__users__by__grid orders__informations">\
                        <p>' + data.data[i].product[j][0] + '<span style=color:red;> x' + data.data[i].product[0][1] + '</span></p>\
                        <p>' + data.data[i].date_ordered + '</p>\
                        <p>' + data.data[i].date_deliverd + '</p>\
                        <p class = "some_need_ful_info">' + data.data[i].transaction_id + '</p>\
                    </div> <br>'
                )
            }

        }
        itsucks()
    })
})




$(".total_orders").click(() => {
    location.reload()
})



function itsucks() {

    $(".fucking__address").hide()

    $("div.orders__informations p.some_need_ful_info").hover(() => {
        var trns_id = $(".orders__informations p.some_need_ful_info:hover").text()
        var url = "/AdminModel/get_address_for_popup/"
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'trns_id': trns_id
            })
        }).then((response) => {
            return response.json()
        }).then((data) => {
            $(".fucking__address").empty()
            $(".fucking__address").append(
                '<p>' + data.data.customer + ', ' + data.data.address + ' , \
             ' + data.data.city + ' - ' + data.data.zipcode + '.\
            </p> '
            )
        })
        $(".fucking__address").toggle()
    })

}
itsucks()




