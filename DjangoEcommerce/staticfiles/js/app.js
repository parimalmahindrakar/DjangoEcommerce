
var address__close__icon = $(".checkout__page__user__address__close__icon");
var address__confirmation__box = $("#checkout__page__user__address__id");


$(".bars").click(() => {
    $(".mobile__nav__fade__and__show__circle").toggleClass("open");
    $(".mobile__nav__fade__and__show").toggleClass("open");
    $(".bars").toggleClass("toggle")
    
})
 

address__close__icon.click(() => {
    address__confirmation__box.toggleClass("close");
    $(".checkout__page__user__address__close__icon").toggleClass("hiding");
    $(".take__up").toggleClass("showing");

})

$(".order__confirmation__msg__div__close__btn").click(() => {
	location.reload()
})



$(window).on("scroll", function (e) {
    e.preventDefault();
    if ($(window).scrollTop()) {
        $(".up__arrow").show();
    }
    else {
        $(".up__arrow").hide();
    }
})

$("a[href='#top']").click(function (e) {
    e.preventDefault();
    $("html, body").animate({ scrollTop: 0 }, "slow");
    return false;
});
   

$(document).ready(
	function () {
		$(".loading-screen").hide()
		var updateBtns = document.getElementsByClassName("update-cart");
		for (var i = 0; i < updateBtns.length; i++) {
			updateBtns[i].addEventListener('click', function () {
				var productid = this.getAttribute("data-product")
				var action = this.getAttribute("data-action")
				var buy = this.getAttribute("data-to-buy")
				if (user === "AnonymousUser") {
					alert("Please login to add items to cart.")
				} else {
					updateUserOrder(productid, action, buy);
				}
			})
		}
		function updateUserOrder(productid, action, buy) {
			var url = "/update/"
			fetch(url, {
				method: 'POST',
				headers: {
					"Content-Type": "application/json",
					'X-CSRFToken': csrftoken
				},
				body: JSON.stringify({
					'productid': productid,
					'action': action
				})
			}).then((response) => {
				return response.json()
			}).then((data) => {
				if (buy == "buy") {
					window.location.href = "/chekcout/"
				} else {
					location.reload()
				}
			})
		}

		var star_rating = $('.star-rating .far');
		var SetRatingStar = function () {
			return star_rating.each(function () {
				if (parseInt(star_rating.siblings('input.rating-value').val()) >= parseInt($(this).data('rating'))) {
					return $(this).removeClass('far fa-star').addClass('fas fa-star');
				} else {
					return $(this).removeClass('fas fa-star').addClass('far fa-star');
				}
			});
		};

		star_rating.on('click', function () {
			star_rating.siblings('input.rating-value').val($(this).data('rating'));
			return SetRatingStar();
		});

		SetRatingStar();

		$("#total-product-image").text($('.product-slider-carousel').length)
		var updateBtns = document.getElementsByClassName("product-slider");
		for (var i = 0; i < updateBtns.length; i++) {
			updateBtns[i].addEventListener('click', function () {
				var to_slide = this.getAttribute("data-slide")
				if (to_slide == "next") {
					$("#current-product-image").text($('div.active').index() + 1)
				}
				else if (to_slide == "prev") {
					var number = $('div.active').index() - 1;
					if (number == -1) {
						$("#current-product-image").text($('.product-slider-carousel').length)
					} else {
						$("#current-product-image").text(number)
					}

				}
			})
		}



		var product_review_button = $("#product-review-button")
		product_review_button.click(() => {
			if (user === "AnonymousUser") {
				alert("Please login to add the review.")
			} else {
				var customer = "{{request.userB}}"
				var product = "{{product.id}}"
				var review = $("#rating-view").val()
				var stars = 5 - $(".fa-star-o").length
				var url = "/update_review/"
				fetch(url, {
					method: 'POST',
					headers: {
						"Content-Type": "application/json",
						'X-CSRFToken': csrftoken
					},
					body: JSON.stringify({
						'customer': customer,
						'productid': product,
						'review': review,
						'stars': stars,
					})
				}).then((response) => {
					return response.json()
				}).then((data) => {
					location.reload()
				})


			}
		}
		)



	}
)