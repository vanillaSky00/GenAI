document.getElementById('postButton').addEventListener('click', function() {
    var postInput = document.getElementById('postInput');
    var postContent = postInput.value;
    if (postContent) {
        var postsContainer = document.getElementById('postsContainer');
        var post = document.createElement('div');
        post.classList.add('post');
        post.innerText = postContent;
        postsContainer.appendChild(post);
        postInput.value = '';
    }
});