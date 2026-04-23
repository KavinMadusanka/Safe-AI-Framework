# ground_truth_19.py
# Hand-verified ground truth for 19_blog_platform.js
#
# Source has:
#   Classes: Post, Comment, IBlogRepository, BlogRepository,
#            BlogService, BlogController, DatabaseConnection
#   Architecture: 4-layer Controller -> Service -> Repository -> DB
#   Language: JavaScript (ES6 classes, extends for inheritance)

SAMPLE   = "19_blog_platform.js"
LANGUAGE = "javascript"

# ── CLASS DIAGRAM ──────────────────────────────────────────────────────────
CLASS_GT = {
    "classes": {
        "Post", "Comment", "IBlogRepository",
        "BlogRepository", "BlogService", "BlogController", "DatabaseConnection"
    },
    "fields": {
        "Post.postId", "Post.title", "Post.authorId",
        "Post.content", "Post.published", "Post.tags",
        "Comment.commentId", "Comment.postId", "Comment.authorId",
        "Comment.text", "Comment.approved",
        "BlogRepository.connection",
        "BlogService.repository",
        "BlogController.service",
        "DatabaseConnection.host", "DatabaseConnection.port",
        "DatabaseConnection.connected",
    },
    "methods": {
        "Post.getPostId", "Post.getTitle", "Post.getAuthorId",
        "Post.getContent", "Post.isPublished", "Post.getTags",
        "Post.setPublished", "Post.setContent", "Post.addTag",
        "Comment.getCommentId", "Comment.getPostId", "Comment.getAuthorId",
        "Comment.getText", "Comment.isApproved",
        "Comment.setApproved", "Comment.setText",
        "IBlogRepository.findPostById", "IBlogRepository.findAllPosts",
        "IBlogRepository.findPostsByAuthor", "IBlogRepository.savePost",
        "IBlogRepository.deletePost", "IBlogRepository.findCommentsByPost",
        "IBlogRepository.saveComment", "IBlogRepository.deleteComment",
        "BlogRepository.findPostById", "BlogRepository.findAllPosts",
        "BlogRepository.findPostsByAuthor", "BlogRepository.savePost",
        "BlogRepository.deletePost", "BlogRepository.findCommentsByPost",
        "BlogRepository.saveComment", "BlogRepository.deleteComment",
        "BlogService.getPost", "BlogService.getAllPosts",
        "BlogService.getPostsByAuthor", "BlogService.createPost",
        "BlogService.publishPost", "BlogService.deletePost",
        "BlogService.addComment", "BlogService.approveComment",
        "BlogService.deleteComment", "BlogService._validatePost",
        "BlogController.handleGetPost", "BlogController.handleGetAllPosts",
        "BlogController.handleGetByAuthor", "BlogController.handleCreatePost",
        "BlogController.handlePublishPost", "BlogController.handleDeletePost",
        "BlogController.handleAddComment", "BlogController.handleDeleteComment",
        "DatabaseConnection.connect", "DatabaseConnection.disconnect",
        "DatabaseConnection.isConnected", "DatabaseConnection.getHost",
        "DatabaseConnection.getPort",
    },
    "relationships": {
        ("implements", "BlogRepository",  "IBlogRepository"),
        ("associates", "BlogRepository",  "DatabaseConnection"),
        ("associates", "BlogService",     "IBlogRepository"),
        ("associates", "BlogController",  "BlogService"),
        ("depends_on", "IBlogRepository", "Post"),
        ("depends_on", "IBlogRepository", "Comment"),
        ("depends_on", "BlogRepository",  "Post"),
        ("depends_on", "BlogRepository",  "Comment"),
        ("depends_on", "BlogService",     "Post"),
        ("depends_on", "BlogService",     "Comment"),
        ("depends_on", "BlogController",  "Post"),
        ("depends_on", "BlogController",  "Comment"),
    }
}
CLASS_VERIFIED = True

# ── PACKAGE DIAGRAM ────────────────────────────────────────────────────────
PACKAGE_GT = {
    "packages": set(),
    "members": {
        "Post", "Comment", "IBlogRepository",
        "BlogRepository", "BlogService", "BlogController", "DatabaseConnection"
    },
    "dependencies": {
        "BlogRepository->IBlogRepository",
        "BlogRepository->DatabaseConnection",
        "BlogService->IBlogRepository",
        "BlogController->BlogService",
    }
}
PACKAGE_VERIFIED = True

# ── SEQUENCE DIAGRAM ───────────────────────────────────────────────────────
SEQUENCE_GT = {
    "participants": {
        "BlogController",
        "BlogService",
        "BlogRepository",
    },
    "key_messages": {
        "BlogController->BlogService:getPost",
        "BlogController->BlogService:createPost",
        "BlogController->BlogService:publishPost",
        "BlogService->BlogRepository:findPostById",
        "BlogService->BlogRepository:savePost",
        "BlogService->BlogRepository:deletePost",
    }
}
SEQUENCE_VERIFIED = True

# ── COMPONENT DIAGRAM ──────────────────────────────────────────────────────
COMPONENT_GT = {
    "components": {
        "Post", "Comment", "IBlogRepository",
        "BlogRepository", "BlogService", "BlogController", "DatabaseConnection"
    },
    "interfaces": {
        "IBlogRepository", "BlogService", "DatabaseConnection"
    },
    "connections": {
        "BlogRepository->DatabaseConnection",
        "BlogService->IBlogRepository",
        "BlogController->BlogService",
    }
}
COMPONENT_VERIFIED = True

# ── ACTIVITY DIAGRAM ───────────────────────────────────────────────────────
ACTIVITY_GT = {
    "actions": {
        "getPost", "getAllPosts", "getPostsByAuthor",
        "createPost", "publishPost", "deletePost",
        "addComment", "deleteComment",
        "findPostById", "savePost",
    },
    "decisions": {
        "more items",
    },
    "swimlanes": set()
}
ACTIVITY_VERIFIED = True