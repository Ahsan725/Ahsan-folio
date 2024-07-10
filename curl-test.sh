#!/bin/bash


BASE_URL="http://127.0.0.1:5000"
POST_ENDPOINT="/api/timeline_post"
GET_ENDPOINT="/api/timeline_post"
DELETE_ENDPOINT="/api/delete_timeline_post"


create_timeline_post() {
    local name="Test User $RANDOM"
    local email="test$user_id@test.com"
    local content="This is a test post created at $(date)"


    echo "Creating Timeline Post:"
    curl -X POST \
        -d "name=$name" \
        -d "email=$email" \
        -d "content=$content" \
        "$BASE_URL$POST_ENDPOINT"
    echo ""
}


get_timeline_posts() {
    # Send GET request using curl
    echo "Retrieving Timeline Posts:"
    curl -X GET "$BASE_URL$GET_ENDPOINT"
    echo ""
}


delete_timeline_posts() {

    echo "Deleting Test Timeline Posts:"
    curl -X DELETE "$BASE_URL$DELETE_ENDPOINT"
    echo ""
}



echo "=== Testing Timeline Post Endpoints ==="
echo ""


create_timeline_post


get_timeline_posts

echo "=== End of Testing ==="
