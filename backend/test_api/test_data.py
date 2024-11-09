expected_groups_response = [
    {
        "id": 1,
        "description": "This is a mock group generated for testing purposes.",
        "name": "Mock Group",
        "persons": [1, 2, 3, 4, 5],
    },
    {
        "id": 2,
        "description": "This is another mock group generated for testing purposes.",
        "name": "Mock Group 2",
        "persons": [6, 7, 8, 9, 10],
    },
]


expected_single_group_response = {
    "description": "This is a mock group generated for testing purposes.",
    "id": 1,
    "name": "Mock Group",
    "persons": [1, 2, 3, 4, 5],
}

expected_create_group_response = {
    "description": "Pytest group description",
    "id": 3,
    "name": "Pytest group name",
    "persons": [],
    "user": 1,
    "user_id": 1,
}


# do we also want to serialize persons as integers here?
expected_update_group_response = {
    "description": "Update group description",
    "id": 1,
    "name": "Update group name",
    "persons": [1, 2, 3, 4, 5],
    "user": 1,
}

expected_delete_group_response = {"message": "Group deleted"}


expected_get_persons_response = [
    {
        "default_image": {
            "blurhash": None,
            "id": 10,
            "url": "https://picsum.photos/seed/prosopagnosia-1-9/1024",
        },
        "default_image_id": 10,
        "first_name": "Sean",
        "groups": [1],
        "id": 1,
        "images": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "last_name": "Green",
        "nick_names": ["Eric", "Allison"],
    },
    {
        "default_image": {
            "blurhash": None,
            "id": 20,
            "url": "https://picsum.photos/seed/prosopagnosia-2-9/1024",
        },
        "default_image_id": 20,
        "first_name": "Tony",
        "groups": [1],
        "id": 2,
        "images": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "last_name": "Hoffman",
        "nick_names": ["Karla", "Nicole"],
    },
    {
        "default_image": {
            "blurhash": None,
            "id": 30,
            "url": "https://picsum.photos/seed/prosopagnosia-3-9/1024",
        },
        "default_image_id": 30,
        "first_name": "Troy",
        "groups": [1],
        "id": 3,
        "images": [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
        "last_name": "Collins",
        "nick_names": ["Steven", "Lisa"],
    },
    {
        "default_image": {
            "blurhash": None,
            "id": 40,
            "url": "https://picsum.photos/seed/prosopagnosia-4-9/1024",
        },
        "default_image_id": 40,
        "first_name": "Nancy",
        "groups": [1],
        "id": 4,
        "images": [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
        "last_name": "Burnett",
        "nick_names": ["Jacob", "Yvonne"],
    },
    {
        "default_image": {
            "blurhash": None,
            "id": 50,
            "url": "https://picsum.photos/seed/prosopagnosia-5-9/1024",
        },
        "default_image_id": 50,
        "first_name": "Cynthia",
        "groups": [1],
        "id": 5,
        "images": [41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
        "last_name": "Miller",
        "nick_names": ["Jessica", "Valerie"],
    },
    {
        "default_image": {
            "blurhash": None,
            "id": 60,
            "url": "https://picsum.photos/seed/prosopagnosia-6-9/1024",
        },
        "default_image_id": 60,
        "first_name": "Richard",
        "groups": [2],
        "id": 6,
        "images": [51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
        "last_name": "Gregory",
        "nick_names": ["Leslie", "Jason"],
    },
    {
        "default_image": {
            "blurhash": None,
            "id": 70,
            "url": "https://picsum.photos/seed/prosopagnosia-7-9/1024",
        },
        "default_image_id": 70,
        "first_name": "Jennifer",
        "groups": [2],
        "id": 7,
        "images": [61, 62, 63, 64, 65, 66, 67, 68, 69, 70],
        "last_name": "Smith",
        "nick_names": ["Mackenzie", "Allison"],
    },
    {
        "default_image": {
            "blurhash": None,
            "id": 80,
            "url": "https://picsum.photos/seed/prosopagnosia-8-9/1024",
        },
        "default_image_id": 80,
        "first_name": "Connor",
        "groups": [2],
        "id": 8,
        "images": [71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
        "last_name": "Wilson",
        "nick_names": ["Debra", "Morgan"],
    },
    {
        "default_image": {
            "blurhash": None,
            "id": 90,
            "url": "https://picsum.photos/seed/prosopagnosia-9-9/1024",
        },
        "default_image_id": 90,
        "first_name": "Joshua",
        "groups": [2],
        "id": 9,
        "images": [81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
        "last_name": "Good",
        "nick_names": ["Craig", "Melissa"],
    },
    {
        "default_image": {
            "blurhash": None,
            "id": 100,
            "url": "https://picsum.photos/seed/prosopagnosia-10-9/1024",
        },
        "default_image_id": 100,
        "first_name": "Randy",
        "groups": [2],
        "id": 10,
        "images": [91, 92, 93, 94, 95, 96, 97, 98, 99, 100],
        "last_name": "Miller",
        "nick_names": ["Joshua", "Shawn"],
    },
]

expected_create_new_person_response = {
    "default_image_id": None,
    "first_name": "Teppo",
    "groups": [],
    "id": 11,
    "images": [],
    "last_name": "Tulppu",
    "nick_names": ["TT", "T-boy"],
    "user": 1,
    "user_id": 1,
}

expected_get_single_person_response = {
    "default_image": {
        "blurhash": None,
        "id": 10,
        "url": "https://picsum.photos/seed/prosopagnosia-1-9/1024",
    },
    "default_image_id": 10,
    "first_name": "Timothy",
    "groups": [1],
    "id": 1,
    "images": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "last_name": "Allen",
    "nick_names": ["Brandon", "Hayden"],
    "user": 1,
    "user_id": 1,
}
