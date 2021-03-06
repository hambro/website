/* Get cookie for POST request with AJAX */
$(document).ready(function () {
    $.ajaxSetup({
        headers: { 'X-CSRFToken': Cookies.get('csrftoken') }
    });
});

/* Filter items by checkboxes */
// creates all items to be remembered with filtering
var cardItemsChildren = document.getElementById("card-items").children;
for (var i = 0; i < cardItemsChildren.length; i++) {
    AllItemList[cardItemsChildren[i].id] = cardItemsChildren[i]
}

function filter_category(checked, category) {
    categoriesFilterd[category] = checked;

    // check if any boxes are clicked
    isActivated = false
    for (key in categoriesFilterd) {
        if (categoriesFilterd[key]) {
            isActivated = true
        }
    }
    var cardItems = document.getElementById("card-items");
    cardItems.innerHTML = '';
    var cardItemsList = [];
    // append only clicked items to list
    if (isActivated) {
        for (var key in AllItemList) {
            var itemCat = key.split('-')[0];
            if (categoriesFilterd[itemCat]) {
                cardItemsList.push(AllItemList[key])
            }
        }
    } else {
        // if no boxes are clicked, all item is presented
        for (var key in AllItemList) {
            cardItemsList.push(AllItemList[key])
        }
    }
    // append the filtered items to parent node
    for (var i = 0; i < cardItemsList.length; i++) {
        cardItems.appendChild(cardItemsList[i])
    }


}

/* User wishes to increment or decrement amount of items added to cart */
//user presses the + button
function plus(item_name, item_pk) {
    item_dict[item_name]++;
    document.getElementById('item_' + item_name).value = item_dict[item_name];
}

// user presses the - button
function minus(item_name, item_pk) {
    if (item_dict[item_name] > 0) {
        item_dict[item_name]--;
    }
    document.getElementById('item_' + item_name).value = item_dict[item_name];
}

function changeQuantity(self, item_name) {

    if (item_dict[item_name] === 0) {
        self.preventDefault();
        return false;
    }
    var id = self.getAttribute("id");
    self.setAttribute("value", id + "-" + item_dict[item_name]);
    return false;
}

function getTotalForItem(item_list_id) {
    let item = document.getElementById(item_list_id);
    let quantity = item.children[1].innerHTML;
    let price = item.children[2].innerHTML;
    let priceWithPoint = price.replace(",", ".");
    return (
        parseFloat(priceWithPoint).toFixed(2)
        * parseFloat(quantity).toFixed(2)
    ).toFixed(2);
}


/* Add a remove item from cart button and if user presses, remove the item */
// Create a "close" button and append it to each list item
var itemList = document.getElementsByClassName("item-list");
// var i;

for (i = 0; i < itemList.length; i++) {
    var columns = itemList[i].children.length;
    // Get total price for items: quantity*price
    itemList[i]
        .children[columns - 2]
        .innerHTML = getTotalForItem(itemList[i].id).replace(".", ",");
}
// Click on a close button to remove the current list item
var closeItem = document.getElementsByClassName("item-list");
var i;
for (i = 0; i < closeItem.length; i++) {
    // The 'x' at the far right
    var close_button = closeItem[i].lastElementChild;
    close_button.onclick = function () {
        // Get the current li element
        var current_item = this.parentNode;
        // Get the id of the li element and put into array
        var item_id_array = current_item.id.split("-");
        // Get item id
        var item_id = item_id_array[item_id_array.length - 1];

        $.ajax({
            type: "POST",
            url: "/kontoret/fjern-vare/" + item_id,
            datatype: "json",

            success: function (json) {
                let total_sum_element = document.getElementById("total-sum-in-cart");
                let sum_to_remove = current_item.
                    children[current_item.children.length - 2]
                    .innerHTML;
                let total_sum = total_sum_element.innerText.split(" ")[1];
                // Nasty, but really just takes the difference between previous total sum
                // and sum of items removed + replaces decimal separator 'dot' to 'comma'
                let new_sum = parseFloat(
                    parseFloat(total_sum).toFixed(2) -
                    parseFloat(sum_to_remove).toFixed(2)
                ).toFixed(2).replace(".", ",");
                if (parseInt(new_sum) == 0) {
                    $.ajax({
                        type: "POST",
                        url: "/kontoret/fjern-handlekurv/",
                        datatype: "json",

                        success: function (json) {
                            window.location.replace(window.location.href.substring(0, window.location.href.length - 1))
                        }
                    })
                }
                total_sum_element.innerHTML = `Total: ${new_sum}`;
                let number_of_items_left = document.getElementsByClassName("item-list").length;
                current_item.parentNode.removeChild(current_item);
                if ((number_of_items_left - 1) === 0) {
                    for (let key in item_dict) {
                        item_dict[key] = 0;
                    }
                    window.location.replace(window.location.href.substring(0, window.location.href.length - 1))
                }
            },

            error: function (xhr, errmsg, err) {
                // console.log(xhr.status + ": " + xhr.responseText);
            },
        });
    }
}
function animateButton() {
    /* Animation for the floating shopping cart button */
    var btnElem = document.getElementsByClassName("btn btn-warning btn-fab")[0];
    var bottomPos = 29; // Same as in the CSS further up
    var animationStep = 0;
    // index 0 is the duration of the movement
    // index 1 is the speed for the movement
    // Each element array represents one movement of the animation
    // First animation up and down
    // Second animation up and down
    var animation = [
        [10, 2], [10, 1], [10, 0], [10, -1], [10, -2],
        [5, 1], [5, 0.5], [5, 0], [5, -0.5], [5, -1],
    ]
    var id = setInterval(frame, 5);
    function frame() {
        if (animationStep == animation.length) {
            // Ends the animates
            clearInterval(id);
        } else {
            speedDuration = animation[animationStep]
            if (speedDuration[0] == 0) {
                // Moves on to the next movement
                animationStep++
            } else {
                bottomPos += speedDuration[1]
                speedDuration[0]--
            }
        }
        btnElem.style.bottom = bottomPos.toString() + ".px"
    }
}
function activatePressForNavigationScrolling() {
    (function ($) {
        $.dragScroll = function (options) {
            var settings = $.extend({
                scrollVertical: true,
                scrollHorizontal: true,
                cursor: null
            }, options);

            var clicked = false,
                clickY, clickX;

            var getCursor = function () {
                if (settings.cursor) return settings.cursor;
                if (settings.scrollVertical && settings.scrollHorizontal) return 'move';
                if (settings.scrollVertical) return 'row-resize';
                if (settings.scrollHorizontal) return 'col-resize';
            }

            var updateScrollPos = function (e, el) {
                $('html').css('cursor', getCursor());
                var $el = $(el);
                settings.scrollVertical && $el.scrollTop($el.scrollTop() + (clickY - e.pageY));
                settings.scrollHorizontal && $el.scrollLeft($el.scrollLeft() + (clickX - e.pageX));
            }

            $(document).on({
                'mousemove': function (e) {
                    clicked && updateScrollPos(e, this);
                    pauseEvent(e)
                },
                'mousedown': function (e) {
                    clicked = true;
                    clickY = e.pageY;
                    clickX = e.pageX;
                },
                'mouseup': function () {
                    clicked = false;
                    $('html').css('cursor', 'auto');
                }
            });
        }
        function pauseEvent(e) {
            if (e.stopPropagation) e.stopPropagation();
            if (e.preventDefault) e.preventDefault();
            e.cancelBubble = true;
            e.returnValue = false;
            return false;
        }
    }(jQuery))

    $.dragScroll();
}

function removeCart() {
    $.ajax({
        type: "POST",
        url: "/kontoret/fjern-handlekurv/",
        datatype: "json",

        success: function (json) {
            var loc = window.location;
            window.location = loc.protocol + '//' + loc.host + loc.pathname + loc.search;
        }
    })
}