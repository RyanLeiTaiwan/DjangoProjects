function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        // Fix occasional csrf_token errors in Chrome:
        // https://piazza.com/class/iy0qa81i5xl1qz?cid=274
        cookies[i] = cookies[i].trim();
        // console.log(cookies[i]);
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}

function sanitize(s) {
    // Be sure to replace ampersand first
    // Yu-Heng Lei: adding my other replacements to resemble Django's filters
    // {{ post.text|nbsp|linebreaksbr }}
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/\r\n/g, '<br>')
            .replace(/\n/g, '<br>')
            .replace(/ /g, '&nbsp;')
            .replace(/\+/g, '&plus;');
}

// Display message in the comment input
function displayLocalMessage(message, post_id) {
    id_message = "#post-" + post_id + "-message";
    $(id_message).html(message);
}

// Display message on top of page
function displayGlobalMessage(message) {
    $("#global-message").html(message);
}

// Send a new request to get the latest posts and comments
function getPostsAndComments(user_id) {
    // @param user_id
    //   0: global stream
    //   -1: following stream
    //   others: get posts of a specific user (in Profile page)
    $.ajax({
        url: "/socialnetwork/get-posts-comments/" + user_id,
        type: "GET",
        dataType : "json",
        success: updatePostsAndComments,
        error: function(xhr) {
            displayGlobalMessage("AJAX error: " + xhr.status + " " + xhr.statusText);
        }
    });
}

function updatePostsAndComments(posts) {
    // Do not remove all existing posts.
    $(posts).each(function() {
        // For a NEW post (whose id does NOT exist in the DOM tree checked by jQuery object length):
        //   "prepend" it to #stream by ascending timestamp (~= Append by descending timestamp)
        var post_id = "#post-" + this.post_id;
        if ($(post_id).length == 0) {
            $("#stream").prepend(
                "<div class='post'>" +
                    "<div class='header-post'>" +
                        "<a href='/socialnetwork/profile/" + this.user_id + "'>" +
                            // Profile picture
                            "<img class='avatar-post' src='/socialnetwork/profile/" + this.user_id + "/pic'>" +
                            "@" + this.username +
                        "</a>&nbsp" + (
                            // Only show a follow/unfollow button for posts by OTHER users
                            this.follow != -1 ? (
                                this.follow == 1 ? (
                                    // "FOLLOW"
                                    // Show follow button
                                    "<form class='posts-follow' action='/socialnetwork/follow/" + this.user_id + "' method='POST'>" +
                                        "<button type='submit' class='btn btn-success btn-xs'>" +
                                            "<span class='glyphicon glyphicon-heart-empty' aria-hidden='true'></span>&nbsp;Follow" +
                                        "</button>" +
                                        // csrf_token (non-AJAX way)
                                        "<input name='csrfmiddlewaretoken' value='" + getCSRFToken() + "' type='hidden'>" +
                                    "</form>"
                                ) : (
                                    // Show unfollow button
                                    "<form class='posts-follow' action='/socialnetwork/unfollow/" + this.user_id + "' method='POST'>" +
                                        "<button type='submit' class='btn btn-danger btn-xs'>" +
                                            "<span class='glyphicon glyphicon-heart' aria-hidden='true'></span>&nbsp;Unfollow" +
                                        "</button>" +
                                        // csrf_token (non-AJAX way)
                                        "<input name='csrfmiddlewaretoken' value='" + getCSRFToken() + "' type='hidden'>" +
                                    "</form>"
                                )
                            ) : ""
                        ) +
                        "<div class='timestamp'>" + this.timestamp + "</div>" +
                    "</div>" +
                    "<div class='content-post'>" +
                        // Sanitize the text for security and desired format
                        // Django template filter: {{ post.text|nbsp|linebreaksbr|urlize }}
                        sanitize(this.text) +
                    "</div>" +

                    // Comment section
                    "<div id='post-" + this.post_id + "' class='comments' >" +
                        // Comment input with onclick event listener
                        "<textarea id='post-" + this.post_id + "-comment' class='comment' placeholder='Write a comment...'></textarea>" +
                        "<button class='btn btn-primary btn-sm' onclick='addComment(" + this.post_id + ")'>Comment</button>" +
                        <!-- Custom per-comment error message for AJAX -->
                        "<div id='post-" + this.post_id + "-message' class='message'></div>" +
                    "</div>" +
                "</div>"
            );
        }

        // For ANY post, "append" each of its NEW comments to #post-id by ascending timestamp
        $(this.comments).each(function() {
            // NEW comment: a comment whose id does NOT exist in the DOM tree checked by jQuery object length
            var comment_id = "#comment-" + this.comment_id;
            if ($(comment_id).length == 0) {
                $(post_id).append(
                    "<div id='comment-" + this.comment_id + "' class='comment'>" +
                        "<a href='/socialnetwork/profile/" + this.user_id + "'>" +
                            "<span>@" + this.username + "</span>" +
                        "</a>&nbsp;" +
                        "<span class='timestamp'>" + this.timestamp + "</span>" +
                        "<div class='header-comment'>" +
                            "<a href='/socialnetwork/profile/" + this.user_id + "'>" +
                                // Profile picture
                                "<img class='avatar-comment' src='/socialnetwork/profile/" + this.user_id + "/pic'>" +
                            "</a>" +
                            "<div class='content-comment'>" +
                                sanitize(this.text) +
                            "</div>" +
                        "</div>" +
                    "</div>"
                )
            }
        });
    });
}

function addComment(post_id) {
    // id: #post-post_id-comment
    var id_input = "#post-" + post_id + "-comment";
    var commentElement = $(id_input);
    // Use encodeURIComponent() to escape special characters like '&' and '+' in the string
    // https://www.w3schools.com/jsref/jsref_encodeURIComponent.asp
    var commentText = encodeURIComponent(commentElement.val());
    console.log("commentElement: " + commentElement);
    console.log("commentText: " + commentText);
    console.log("param_user_id: " + param_user_id);

    // Clear old error message (if any)
    displayGlobalMessage("");
    // Assume valid post_id
    displayLocalMessage("", post_id);

    $.ajax({
        url: "/socialnetwork/comment/" + post_id + "/" + param_user_id,
        type: "POST",
        data: "text=" + commentText + "&csrfmiddlewaretoken=" + getCSRFToken(),
        dataType : "json",
        success: function(response) {
            // console.log(response);
            if (Array.isArray(response)) {
                // Clear comment input only on validation success
                commentElement.val("");
                updatePostsAndComments(response);
            } else {
                if (commentElement.length != 1) {
                    // When the post_id is not even valid
                    displayGlobalMessage(response.error);
                } else {
                    displayLocalMessage(response.error, post_id);
                }
            }
        },
        error: function(xhr) {
            displayGlobalMessage("AJAX error: " + xhr.status + " " + xhr.statusText);
        }
    });
}

// Sorry, I have to maintain a global variable for the parameter user_id in get_posts_comments()
// such that addComment knows "how" to call get_posts_comments() for global stream / following stream / profile pages
// Leaving it as a parameter in addComment() is "insecure" because the user may modify HTML code to mess up the page
param_user_id = -2;

// Call two JavaScript (AJAX) functions on page load
// 1. The posts.html does not load the posts, so we call getPosts()
//    as soon as page is finished loading
// 2. Update the stream every 5 seconds
function init(user_id) {
    param_user_id = user_id;
    getPostsAndComments(user_id);
    window.setInterval(function() { getPostsAndComments(user_id); }, 5000);
}
