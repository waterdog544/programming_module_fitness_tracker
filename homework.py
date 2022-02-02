from typing import Dict, Union


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        text: str = (f'Тип тренировки: {self.training_type}; '
                     f'Длительность: {self.duration:.3f} ч.; '
                     f'Дистанция: {self.distance:.3f} км; '
                     f'Ср. скорость: {self.speed:.3f} км/ч; '
                     f'Потрачено ккал: {self.calories:.3f}.')
        return text


class Training:
    """Базовый класс тренировки."""

    TRAINING_TYPE: str = ''     # type of training
    LEN_STEP: float = 0.65      # lenght of step
    M_IN_KM: int = 1000         # transformation metre in kilometre
    H_IN_MIN: int = 60          # transformation hour in minute

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message_1: InfoMessage = InfoMessage(self.TRAINING_TYPE,
                                             self.duration,
                                             self.get_distance(),
                                             self.get_mean_speed(),
                                             self.get_spent_calories())
        return message_1


class Running(Training):
    """Тренировка: бег."""
    TRAINING_TYPE: str = 'Running'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coef_calorie_1: int = 18
        coef_calorie_2: int = 20
        spent_calories: float = ((coef_calorie_1 * self.get_mean_speed()
                                 - coef_calorie_2) * self.weight
                                 / self.M_IN_KM * self.duration
                                 * self.H_IN_MIN)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    TRAINING_TYPE: str = 'SportsWalking'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coef_cal_1: float = 0.035
        coef_cal_2: int = 2
        coef_cal_3: float = 0.029
        spent_cal: float = ((coef_cal_1 * self.weight
                            + (self.get_mean_speed()**coef_cal_2
                               // self.height) * coef_cal_3 * self.weight)
                            * self.duration * self.H_IN_MIN)
        return spent_cal


class Swimming(Training):
    """Тренировка: плавание."""
    TRAINING_TYPE: str = 'Swimming'
    LEN_STEP: float = 1.38  # lenght of step

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.LEN_STEP / self.M_IN_KM * self.action
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (self.length_pool * self.count_pool /
                             self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coef_cal_1: float = 1.1
        coef_cal_2: int = 2
        spent_calories: float = ((self.get_mean_speed() + coef_cal_1) *
                                 coef_cal_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    # Compration code of workout type and Class
    workout_type_dict: Dict[str,
                            Union[Running,
                                  SportsWalking,
                                  Swimming
                                  ]
                            ] = {'SWM': Swimming,
                                 'RUN': Running,
                                 'WLK': SportsWalking
                                 }

    one: Training = workout_type_dict[workout_type](*data)
    return one


def main(training: Training) -> None:
    """Главная функция."""
    # get object InfoMessage
    info: InfoMessage = Training.show_training_info(training)
    print(info.get_message())
    pass


# test with existent data
if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
