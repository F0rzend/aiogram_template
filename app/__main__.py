from app.main import main
from app.utils.logger import configure_logger

if __name__ == '__main__':
    configure_logger("DEBUG", ['aiogram', 'aiogram.dispatcher.dispatcher'])
    main()
