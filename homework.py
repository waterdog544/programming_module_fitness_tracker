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
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    TRAINING_TYPE = ''
    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_MIN = 60

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=self.TRAINING_TYPE,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    TRAINING_TYPE = 'Running'
    COEF_CAL_1 = 18
    COEF_CAL_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((Running.COEF_CAL_1 * self.get_mean_speed()
                - Running.COEF_CAL_2) * self.weight
                / self.M_IN_KM * self.duration
                * self.H_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    TRAINING_TYPE = 'SportsWalking'
    COEF_CAL_1 = 0.035
    COEF_CAL_2 = 2
    COEF_CAL_3 = 0.029

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
        return ((SportsWalking.COEF_CAL_1 * self.weight
                + (self.get_mean_speed()**SportsWalking.COEF_CAL_2
                   // self.height) * SportsWalking.COEF_CAL_3 * self.weight)
                * self.duration * self.H_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание."""
    TRAINING_TYPE = 'Swimming'
    LEN_STEP = 1.38
    COEF_CAL_1 = 1.1
    COEF_CAL_2 = 2

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
        return self.LEN_STEP / self.M_IN_KM * self.action

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + Swimming.COEF_CAL_1)
                * Swimming.COEF_CAL_2 * self.weight)


WORKOUT_TYPE_DICT = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking
                     }


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in WORKOUT_TYPE_DICT:
        raise NotImplementedError(f'Определите {workout_type}'
                                  ' в WORKOUT_TYPE_DICT')
    return WORKOUT_TYPE_DICT[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = Training.show_training_info(training)
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type=workout_type, data=data)
        main(training)
