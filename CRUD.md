await User.create(username="alice", email="alice@example.com", age=30)
users_data = [
    {"username": "user1", "email": "user1@example.com", "age": 20},
    {"username": "user2", "email": "user2@example.com", "age": 25},
]
await User.bulk_create([User(**data) for data in users_data])

await User.filter(is_active=False).delete()

await User.filter(id=user_id).update(**kwargs)

await User.filter(username__icontains=username_pattern)
offset = (page - 1) * page_size
await User.all().order_by('-created_at').offset(offset).limit(page_size)


# 问题：多个请求同时更新同一记录可能导致数据不一致
# 解决：使用版本号或时间戳进行乐观锁控制
async def concurrent_safe_update(user_id, expected_version, **kwargs):
    updated_count = await User.filter(id=user_id, version=expected_version).update(version=expected_version + 1, **kwargs)
    if updated_count == 0:
        raise Exception("数据已被其他用户修改，请刷新后重试")

# 问题：一次性加载大量数据导致内存溢出
async def good_batch_process():
    async for user in User.all().iterator():
        # 逐条处理，避免内存溢出
        await process_user(user)

