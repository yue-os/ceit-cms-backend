import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models import User, Role, Permission


async def seed_db():
    async with AsyncSessionLocal() as db:

        try:

            # Check and add roles
            roles_data = [
                {"name": "super_admin", "description": "Super Admin"},
                {"name": "author_ce", "description": "Civil Engineering Author"},
                {"name": "author_ee", "description": "Electrical Engineering Author"},
                {"name": "author_it", "description": "Information Technology Author"},
            ]
            for role_data in roles_data:
                existing_role = (await db.execute(select(Role).filter(Role.name == role_data["name"]))).scalars().first()
                if not existing_role:
                    db.add(Role(name=role_data["name"], description=role_data["description"]))
                    print(f"✅ Role '{role_data['name']}' added.")
                else:
                    print(f"ℹ️  Role '{role_data['name']}' already exists.")
            
            await db.commit()

            # Check and add permissions
            permission_names = [
                "user.manage",
                "article.create",
                "article.archive",
                "article.approve",
                "article.update",
            ]
            for perm_name in permission_names:
                existing_perm = (await db.execute(select(Permission).filter(Permission.name == perm_name))).scalars().first()
                if not existing_perm:
                    db.add(Permission(name=perm_name))
                    print(f"✅ Permission '{perm_name}' added.")
                else:
                    print(f"ℹ️  Permission '{perm_name}' already exists.")

            await db.commit()

            # Assign permissions to roles
            role_permissions_map = {
                "super_admin": permission_names,  # All permissions
                "author_ce": ["article.create", "article.update"],
                "author_ee": ["article.create", "article.update"],
                "author_it": ["article.create", "article.update"],
            }
            for role_name, perms in role_permissions_map.items():
                role = (await db.execute(
                    select(Role).filter(Role.name == role_name).options(selectinload(Role.permissions))
                )).scalars().first()
                if role:
                    for perm_name in perms:
                        permission = (await db.execute(select(Permission).filter(Permission.name == perm_name))).scalars().first()
                        if permission and permission not in role.permissions:
                            role.permissions.append(permission)
                            print(f"✅ Permission '{perm_name}' assigned to role '{role_name}'.")
                    await db.commit()

            # Seed users for each role
            users_to_seed = [
                {
                    "email": "admin@ceit.edu",
                    "first_name": "Super",
                    "last_name": "Admin",
                    "role_name": "super_admin",
                },
                {
                    "email": "ce.author@ceit.edu",
                    "first_name": "Civil",
                    "last_name": "Engineer",
                    "role_name": "author_ce",
                },
                {
                    "email": "ee.author@ceit.edu",
                    "first_name": "Electrical",
                    "last_name": "Engineer",
                    "role_name": "author_ee",
                },
                {
                    "email": "it.author@ceit.edu",
                    "first_name": "IT",
                    "last_name": "Specialist",
                    "role_name": "author_it",
                },
            ]

            for user_data in users_to_seed:
                existing_user = (await db.execute(select(User).filter(User.email == user_data["email"]))).scalars().first()
                
                if not existing_user:
                    role = (await db.execute(select(Role).filter(Role.name == user_data["role_name"]))).scalars().first()
                    
                    if role:
                        new_user = User(
                            email=user_data["email"],
                            first_name=user_data["first_name"],
                            last_name=user_data["last_name"],
                            role_id=role.id,
                            hashed_password=get_password_hash("Admin123!")
                        )

                        db.add(new_user)
                        await db.commit()
                        print(f"✅ {user_data['role_name']} user ({user_data['email']}) seeded.")
                else:
                    print(f"ℹ️  User '{user_data['email']}' already exists.")

            print("✅ Database seeding completed.")

        except Exception as e:
            print(f"Error seeding database: {e}")
            await db.rollback()


if __name__ == "__main__":
    asyncio.run(seed_db())
