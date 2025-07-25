# Architecture

## SeaWolves Pattern

The Calendar API implements the **SeaWolves architecture pattern**, which provides clean separation of concerns and maintainable code structure.

## Layer Description

### 1. Route Layer
**Location**: `routers/calendar.py`

**Responsibilities**:
- HTTP request/response handling
- Input validation using Pydantic models
- Query parameter parsing
- Response model definition

**Example**:
```python
@calendar_router.get("/Calendar", response_model=List[AcceptedEventData])
def get_calendar(
    tf_days: int = Query(default=0),
    after_days: int = Query(default=0),
    db: Session = Depends(get_db)
) -> List[AcceptedEventData]:
    calendar_dal = CalendarDAL(db_session=db)
    calendar_control = CalendarControl(db_session=db, calendar_dal=calendar_dal)
    
    return calendar_control.get_calendar_events(
        tf_days=tf_days,
        after_days=after_days
    )
```

### 2. Control Layer
**Location**: `controls/calendar/Calendar_controls.py`

**Responsibilities**:
- Business logic implementation
- Error handling and validation
- Data transformation
- Coordination between DAL and Route layers

**Example**:
```python
def get_calendar_events(self, tf_days: int, after_days: int) -> List[AcceptedEventData]:
    try:
        return self.calendar_dal.get_events_by_date_range(tf_days, after_days)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Нет событий за указанную дату!"
        )
```

### 3. DAL Layer
**Location**: `db/calendar/Calendar_DAL.py`

**Responsibilities**:
- Database operations
- SQL query construction
- Raw data to model transformation
- Database session management

**Example**:
```python
def get_events_by_date_range(self, tf_days: int, after_days: int) -> List[AcceptedEventData]:
    actual_tf_days = 1 if tf_days == 0 else tf_days
    actual_after_days = 7 if after_days == 0 else after_days
    
    start_date = datetime.now() + timedelta(days=actual_tf_days)
    end_date = datetime.now() + timedelta(days=actual_after_days)
    
    query = select(Event).where(
        Event.start > start_date,
        Event.start < end_date
    )
    
    events = self.db_session.execute(query).scalars().all()
    return [AcceptedEventData.model_validate(event) for event in events]
```

## Data Models

### Input Models
Used for request validation and parameter parsing:

```python
class EventGetByDateRange(BaseModel):
    tf_days: int = Field(default=0)
    after_days: int = Field(default=0)

class EventCreate(BaseModel):
    Start: Optional[int] = Field(default=None)
    Name: str = Field(...)
    Note: Optional[str] = Field(default=None)
    Type: int = Field(default=0)
```

### Response Models
Used for API responses with the `Accepted` prefix:

```python
class AcceptedEventData(TunedModel):
    id: int
    start: datetime 
    name: str
    note: Optional[str] = None
    type: int

class AcceptedEventCreated(TunedModel):
    message: str
```

### Database Models
SQLAlchemy models for database schema:

```python
class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    start = Column(DateTime, nullable=False, index=True)
    name = Column(String, nullable=False)
    note = Column(String, nullable=True)
    type = Column(Integer, nullable=False)
```

## Benefits

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Testability**: Easy to unit test each layer independently
3. **Maintainability**: Clear structure makes code easy to modify
4. **Scalability**: Can easily add new features following the same pattern
5. **Type Safety**: Full type hints and Pydantic validation

## Database Connection

The application uses dependency injection for database sessions:

```python
def get_db() -> Generator:
    """Dependency для получения сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

This ensures proper session management and connection pooling.
