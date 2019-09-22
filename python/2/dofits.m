clc,clear,close all;
filename = '2.fits';
fr_id = fopen(filename,'r','s'); %FITfile
info=fitsinfo(filename); 
cols =info.PrimaryData.Size(1);
rows =info.PrimaryData.Size(2);
oset=info.PrimaryData.Offset;

SIZE_UNIT = 2880;
SIZE_TYPE_NAME= 8;
SIZE_TYPE = 80;
num_type_prim = oset;

for i=1:num_type_prim
   fseek(fr_id, (i-1)*SIZE_TYPE,-1);
   type_name = fread(fr_id, SIZE_TYPE_NAME,'*char');
   switch type_name'
        case 'BITPIX  ' %data dispersion
            fseek(fr_id,2,0); %skip two bytes,cause there are '= ' after type_name
            str_tmp = fread(fr_id, SIZE_TYPE -SIZE_TYPE_NAME - 2,'*char');
            data_percision = str2num(str_tmp(1:20)');
            data_percision = abs(data_percision);
        case 'CRVAL1  '  %thestart position of lamda
            fseek(fr_id,2,0);
            str_tmp = fread(fr_id, SIZE_TYPE -SIZE_TYPE_NAME - 2,'*char');
            lamda_start =str2num(str_tmp(1:20)');
        case 'CD1_1   ' %the step of lamda
            fseek(fr_id,2,0);
            str_tmp = fread(fr_id, SIZE_TYPE -SIZE_TYPE_NAME - 2,'*char');
            lamda_deta =str2num(str_tmp(1:20)');
   end
end

lamda = lamda_start:lamda_deta:lamda_start+lamda_deta*(cols-1);
%%
for i=1:length(lamda)
   lamda(i) = 10^lamda(i);
end

fph_id =fopen('primary_head_info.txt','w','b');
fseek(fr_id,0,-1);
for i=1:num_type_prim
   head_info = fread(fr_id,SIZE_TYPE);
   fwrite(fph_id,head_info);
   fprintf(fph_id,'\r\n');
end
fclose(fph_id);
%%
