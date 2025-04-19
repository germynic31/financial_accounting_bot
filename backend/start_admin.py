import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from admin_panel.admin import (
    CategoryAdmin,
    LimitAdmin,
    TransactionAdmin,
    UserAdmin,
)
from core.database import engine

app = FastAPI()
admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(TransactionAdmin)
admin.add_view(LimitAdmin)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
