from dotenv import load_dotenv
load_dotenv()
from action import perform  # noqa: E402
from edit import SerialEdits  # noqa: E402

operation: SerialEdits = perform()
operation.finish()
