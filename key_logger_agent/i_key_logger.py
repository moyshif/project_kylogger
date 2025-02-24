from abc import ABC, abstractmethod


class IKeyLogger(ABC):
    """
    ממשק מופשט עבור לוגר מקלדת.
    מגדיר את הפעולות הנדרשות לכל יישום של לוגר מקלדת.
    """

    @abstractmethod
    def start_logging(self) -> None:
        """מתחיל את תהליך הרישום של לחיצות מקלדת."""
        pass

    @abstractmethod
    def stop_logging(self) -> None:
        """מפסיק את תהליך הרישום של לחיצות מקלדת."""
        pass

    @abstractmethod
    def get_logged_keys(self):
        """
        מחזיר את רשימת הלחיצות שנרשמו.

        Returns:
            List[Dict[str, Dict[str, str]]]: רשימה של מילונים, כאשר כל מילון מייצג רישום
                                             עבור חלון פעיל, הכולל את הטקסט שנרשם ואת שפת המקלדת.
        """
        pass
