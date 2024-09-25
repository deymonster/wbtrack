import { z } from "zod";

export const LoginAdminSchema = z.object({
    email: z.string().email({ message: "Введите корректный email" }),
    password: z.string().min(1, { message: "Пароль не должен быть пустым" }),
});


export const SignupAdminSchema = z.object({
    email: z.string().email({ message: "Введите корректный email" }).trim(),
    password: z
        .string()
        .min(1, { message: "Пароль не должен быть пустым" })
        .min(8, { message: "Пароль должен содержать не менее 8 символов" })
        .max(32, { message: "Пароль должен содержать не более 32 символов" })
        .regex(/(?=.*[a-z])/, {
            message: "Пароль должен содержать хотя бы 1 строчную букву"})
        .regex(/[^a-zA-Z0-9]/, {
            message: "Пароль должен содержать хотя бы 1 специальный символ"
        })
        .trim(),

});

export type FormState = 
    | {
        errors?: {
            email?: string[];
            password?: string[];
        };
        message?: string;
    }
    | undefined
    