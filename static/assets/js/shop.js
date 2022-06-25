$(document).ready(
    function () {
        $(".cart-btn-js").click(function (e) {
            e.preventDefault();
            const itemid = $(this).attr("itemid").slice(14);
            $("#cart-form input[name=itemid]").val(itemid);
            console.log($("#cart-form input[name=itemid]").val());
            const serializedData = $("#cart-form").serialize();
            $.ajax({
                type: 'POST',
                url: cart_url,
                data: serializedData,
                success: (response) => {
                    let btn = $("[itemid=" + response["product_button_id"] + "]")
                    if (response["added_in_cart"]) {
                        btn.addClass("btn-primary")
                        btn.removeClass('btn-outline-primary')
                        btn.text("Added to Cart")
                        $("#cart").html('Cart <i class="fa fa-cart-plus"></i> ' + response["number_of_items"])
                    }
                    else {
                        btn.removeClass("btn-primary")
                        btn.addClass('btn-outline-primary')
                        btn.text("Add to Cart")
                        $("#cart").html('Cart <i class="fa fa-cart-plus"></i> ' + response["number_of_items"])
                    }
                }
            });
        });
    }
);
