class Match:
    match = None
    mercenary = None
    def __init__(self):
        Match.mercenary = [
            {
                "mercenary_id": 1,
                "name": "Xác sống",
                "price" : 300,
                "attack" : 500,
                "description": "Dường như không có trí tuệ, không phân biệt địch ta!"
            },
            {
                "mercenary_id": 2,
                "name": "Cỗ máy",
                "price": 500,
                "attack": 300,
                "description": "Luôn hoạt động ổn định, được lập trình bởi Trương Văn Công!!!"
            },
            {
                "mercenary_id": 3,
                "name": "Nhẫn giả",
                "price": 1000,
                "attack": 1000,
                "description": "Sức tấn công ưu việt trong tất cả lính đánh thuê!!!"
            },
            {
                "mercenary_id": 4,
                "name": "Hiệp sĩ",
                "price": 2000,
                "attack" : 500,
                "description": "Hiệp sĩ luôn trung thành. Mua năm hiệp sĩ sẽ thắng!!!"
            }
        ]
        Match.match = {
            "match_id": 1,
            "turn_id": 0,
            "user_id": 1,
            "user_roll": 0,
            "roll": 0,
            "dice": 1,
            "request_item_id": 0,
            "users": [
                {
                    "user_id": 1,
                    "hp": 2000,
                    "gold": 0,
                    "position": {
                        "x": 40,
                        "y": 80
                    },
                    "index": 1
                },
                {
                    "user_id": 2,
                    "hp": 2200,
                    "gold": 0,
                    "position": {
                        "x": 40,
                        "y": 80
                    },
                    "index": 1
                }
            ],
            "move_positions": [],
            "items": [
                # {
                #     "item_id": 1,
                #     "attack": 200,
                #     "position": {
                #         "x": 40,
                #         "y": 80
                #     },
                #     "user_id": 1,
                #     "index": 1
                # }
            ],
            "positions": [
                {
                    "position": {
                        "x": 40.0,
                        "y": 80
                    },
                    "index": 1
                },
                {
                    "position": {
                        "x": 40.0,
                        "y": 180
                    },
                    "index": 2
                },
                {
                    "position": {
                        "x": 40.0,
                        "y": 280
                    },
                    "index": 3
                },
                {
                    "position": {
                        "x": 40.0,
                        "y": 380
                    },
                    "index": 4
                },
                {
                    "position": {
                        "x": 40.0,
                        "y": 480
                    },
                    "index": 5
                },
                {
                    "position": {
                        "x": 40.0,
                        "y": 580
                    },
                    "index": 6
                },
                {
                    "position": {
                        "x": 140.0,
                        "y": 580
                    },
                    "index": 7
                },
                {
                    "position": {
                        "x": 240.0,
                        "y": 580
                    },
                    "index": 8
                },
                {
                    "position": {
                        "x": 340.0,
                        "y": 580
                    },
                    "index": 9
                },
                {
                    "position": {
                        "x": 440.0,
                        "y": 580
                    },
                    "index": 10
                },
                {
                    "position": {
                        "x": 540.0,
                        "y": 580
                    },
                    "index": 11
                },
                {
                    "position": {
                        "x": 640.0,
                        "y": 580
                    },
                    "index": 12
                },
                {
                    "position": {
                        "x": 740.0,
                        "y": 580
                    },
                    "index": 13
                },
                {
                    "position": {
                        "x": 740.0,
                        "y": 480
                    },
                    "index": 14
                },
                {
                    "position": {
                        "x": 740.0,
                        "y": 380
                    },
                    "index": 15
                },
                {
                    "position": {
                        "x": 740.0,
                        "y": 280
                    },
                    "index": 16
                },
                {
                    "position": {
                        "x": 740.0,
                        "y": 180
                    },
                    "index": 17
                },
                {
                    "position": {
                        "x": 740.0,
                        "y": 80
                    },
                    "index": 18
                },
                {
                    "position": {
                        "x": 640.0,
                        "y": 80
                    },
                    "index": 19
                },
                {
                    "position": {
                        "x": 540.0,
                        "y": 80
                    },
                    "index": 20
                },
                {
                    "position": {
                        "x": 440.0,
                        "y": 80
                    },
                    "index": 21
                },
                {
                    "position": {
                        "x": 340.0,
                        "y": 80
                    },
                    "index": 22
                },
                {
                    "position": {
                        "x": 240.0,
                        "y": 80
                    },
                    "index": 23
                },
                {
                    "position": {
                        "x": 140.0,
                        "y": 80
                    },
                    "index": 24
                }
            ]
        }
# Match()
# Match.match['match_id'] = 3
# print(Match.match['users'][0]['user_id'])
#
# for user in Match.match['users']:
#     user_id = user['user_id']
#     hp = user['hp']
#     gold = user['gold']
#     position = user.get('position')
#     x = position['x']
#     y = position['y']
#     index = user['index']
#
#     print(f"User ID: {user_id}")
#     print(f"HP: {hp}")
#     print(f"Gold: {gold}")
#     print(f"Current Position (x, y): ({x}, {y})")
#     print(f"Index: {index}")
#     print("")
# positions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
# current_position = 22
# random_number = 6
#
# selected_positions = []
#
# for i in range(current_position + 1, current_position + random_number + 1):
#     position_index = (i - 1) % len(positions)
#     selected_positions.append(positions[position_index])
#
# print(selected_positions)