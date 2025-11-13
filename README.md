# Simple Bank CLI - 命令行银行账户管理系统

一个采用模块化设计的轻量银行账户管理工具，支持开户、存款、取款、余额查询等核心功能，分为安全版（生产可用）和漏洞版（用于安全学习），便于对比理解代码安全实践。


## 项目架构
项目拆分为5个低耦合模块，每个模块职责单一，符合“单一职责原则”：
- `db.py`：数据库访问层（封装SQL操作）
- `models.py`：数据模型定义（Account实体）
- `services.py`：业务逻辑层（核心功能+校验）
- `cli.py`：命令行交互入口（用户操作解析）
- `main.py`：测试脚本（快速验证功能）


## 模块详情
### 1. db.py - 数据库访问层
#### 安全版（推荐生产/测试使用）
- 核心职责：封装SQLite连接与CRUD，通过参数化查询抵御SQL注入
- 关键函数：
  - `get_conn()`：返回带`row_factory=sqlite3.Row`的连接，支持按字段名访问
  - `init_db()`：自动创建`accounts`表（不存在时）
  - `create_account(username, initial_balance)`：参数化插入新账户
  - `get_account_by_username(username)`：参数化查询账户
  - `update_balance(account_id, new_balance)`：参数化更新余额
  - `list_accounts()`：查询所有账户并返回列表
- 安全要点：
  - 所有SQL操作使用`?`占位符参数化，杜绝字符串拼接
  - 用`with get_conn()`或`conn.commit()`管理事务，保证数据一致性
  - `sqlite3.Row`提升数据读取可读性，避免字段索引依赖


---

### 2. models.py - 数据模型定义
#### 安全版
- 核心职责：用`dataclass`定义Account实体，统一数据传递格式
- 关键实现：
  ```python
  from dataclasses import dataclass

  @dataclass
  class Account:
      id: int
      username: str
      balance: float
  ```
- 优势：自动生成`__init__`/`__repr__`方法，简化测试与数据传递


---

### 3. services.py - 业务逻辑层
#### 安全版
- 核心职责：实现开户、存款、取款等业务，包含参数校验与异常处理
- 关键函数：
  - `open_account(username, initial_balance)`：校验账户是否已存在，创建合法账户
  - `get_account(username)`：查询账户并返回Account实例
  - `deposit(username, amount)`：校验存款金额>0，更新余额
  - `withdraw(username, amount)`：校验取款金额>0且余额充足
- 安全要点：
  - 自定义异常类：`AccountExistsError`（重复开户）、`InsufficientFundsError`（余额不足）
  - 严格参数校验：拒绝负数存款/取款，转换金额为float确保计算一致性
  - 依赖`db.py`的参数化操作，不直接处理SQL


---

### 4. cli.py - 命令行交互入口
#### 安全版
- 核心职责：提供REPL交互，解析用户命令并调用业务逻辑
- 支持命令：
  - `init`：初始化数据库表
  - `create <username> [initial]`：开户（默认初始余额0）
  - `deposit <username> <amount>`：存款
  - `withdraw <username> <amount>`：取款
  - `balance <username>`：查询余额
  - `list`：列出所有账户
  - `help`：查看命令帮助
  - `exit`：退出程序
- 安全要点：
  - 启动时自动调用`init_db()`，确保表存在
  - 对命令参数长度、类型做基础校验（如转换amount为float）
  - `try/except`捕获业务异常，向用户输出友好提示（而非报错堆栈）


---

### 5. main.py - 冒烟测试脚本
#### 安全版
- 核心职责：自动化执行关键功能测试，快速验证逻辑正确性
- 实现细节：
  - 自动初始化数据库，执行开户、存款、取款、重复开户等场景
  - 包装异常确保测试脚本不中断，输出每个步骤的执行结果
  - 打印账户状态变化，便于验证功能是否符合预期


## 使用指南
### 环境要求
- Python 3.7+（依赖`dataclasses`模块，3.7+内置）
- 无额外第三方依赖（使用标准库`sqlite3`）

### 运行安全版
1. 执行命令行交互：
   ```bash
   python cli.py
   ```
2. 运行冒烟测试：
   ```bash
   python main.py
   ```
