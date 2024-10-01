import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { ApiError } from '@/app/shared/api';



const errorMessages: Record<string, string> = {
    "REGISTER_USER_ALREADY_EXISTS": "Пользователь с такой электронной почтой уже существует.",
    "DEFAULT_ERROR": "Произошла ошибка. Пожалуйста, попробуйте еще раз позже.",
    //TODO: add more error messages
};

export const handleApiError = (error: ApiError) => {
    let errorMessage = errorMessages["DEFAULT_ERROR"];

    if (error instanceof ApiError) {
        if (error.body && error.body.detail) {
            errorMessage = errorMessages[error.body.detail] || error.statusText || errorMessages["DEFAULT_ERROR"];
        } else {
            errorMessage = error.statusText || errorMessages["DEFAULT_ERROR"];
        }
    } else if (typeof error === 'string') {
        errorMessage = error;
    }
    toast.error("Ошибка: " + errorMessage);
    console.error("Ошибка:", error);
};

