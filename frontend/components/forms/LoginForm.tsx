"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";

import { useAppContext } from "@/app/context";
import { FcUnlock } from "react-icons/fc";

const LoginForm = () => {

  const { login } = useAppContext();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (event: React.FormEvent) => {
    event.preventDefault();
    await login(username, password);
  };

  return (
    <form onSubmit={handleLogin}>
                    
      <Label htmlFor="email">Email</Label>
          <Input 
          className="mt-2 mb-4 bg-transparent rounded-full"
          type="email" 
          id="email"
          name="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="vasya_pupkin@pisem.net"/>
                    
      <Label htmlFor="password">Password</Label>
        <Input 
        className="mt-2 mb-4 bg-transparent rounded-full"
        type="password" 
        id="password" 
        name="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="••••••••"/>

      <Button 
        type="submit" 
        className="flex items-center gap-4 px-12 w-full mt-6 mb-6 bg-indigo-600 rounded-full hover:bg-indigo-700"
        variant="outline"
        >
            <FcUnlock size={26}/>
            Войти в АйТи
      </Button>
    </form>
  )

};

export default LoginForm;