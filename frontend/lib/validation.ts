import { z } from "zod";

export const EmployeeFormValidation = z.object({
    phone: z.string().refine((phone) => /^\+\d{10,15}$/.test(phone), 'Некорретный формат номера'),
})



export const RegisterAdminFormValidation = z.object({
    email: z.string().email({ message: "Введите корректный email" }),
    password: z.string()
        .min(1, { message: "Пароль не должен быть пустым" })
        .regex(/[a-z]/, { message: "Пароль должен содержать хотя бы одну строчную букву"})
        .regex(/[A-Z]/, { message: "Пароль должен содержать хотя бы одну заглавную букву" })
        .regex(/\d/, { message: "Пароль должен содержать хотя бы одну цифру" })
        .regex(/[\W_]/, { message: "Пароль должен содержать хотя бы один специальный символ" }),
    confirmPassword: z.string(),
    first_name: z.string().min(1, { message: "Введите имя" }).optional(),
    middle_name: z.string().optional(),
    last_name: z.string().optional(),
    phone: z.string().refine((phone) => /^\+\d{10,15}$/.test(phone), 'Некорретный формат номера').optional(),
}).refine(data => data.password === data.confirmPassword, {
    message: "Пароли не совпадают",
    path: ["confirmPassword"],
})