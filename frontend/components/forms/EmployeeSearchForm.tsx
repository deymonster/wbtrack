import React, { useState } from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Input } from '../ui/input';
import { Button } from '../ui/button';


interface EmployeeSearchFormProps {
    onSearch: (params: { searchField: string; searchValue: string }) => void;
  }

export const EmployeeSearchForm: React.FC<EmployeeSearchFormProps> = ({ onSearch }) =>{
    const [searchField, setSearchField] = useState<string>('');
    const [searchValue, setSearchValue] = useState<string>('');

    const handleSearch = () => {
        if (searchValue.trim()){
            onSearch({searchField, searchValue });
        }
    };

    return (
        <div className='flex item-center py-4 space-x-4'>
            <Select
            value={searchField}
            onValueChange={(value)=> setSearchField(value)}
            >
                <SelectTrigger className='w-[150px]'>
                    <SelectValue placeholder="Фильтр поиска"/>
                </SelectTrigger>
                <SelectContent side='top'>
                    <SelectItem value='last_name'>Фамилия</SelectItem>
                    <SelectItem value='phone'>Телефон</SelectItem>
                </SelectContent>
            </Select>
            
            <Input
                placeholder={
                    searchField === 'last_name'
                    ? 'Поиск по фамилии'
                    : 'Поиск по телефону'
                }
                value={searchValue}
                onChange={(event)=> setSearchValue(event.target.value)}
                onKeyDown={(e)=>{
                    if (e.key == 'Enter') {
                        handleSearch();
                    }
                }}
                className='max-w-sm'
            />
            <Button onClick={handleSearch}>Поиск</Button>
        </div>
    )
}