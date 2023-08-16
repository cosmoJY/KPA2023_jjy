% [�ѱ��ɸ���ȸ] ���α׷��� ����, ȭ�� ��� ��, �ü���� ���� �ð� �ڱ� ���� ��Ȯ�� ��
% ����: word3276@gmail.com

% MATLAB R2022b & Psychtoolbox 3.0.19
% ����: �Է�â�� �Ķ���� �Է� > 'Press Z' ������ �߸� zŰ(��� 1) > �ڱ� ���� �� �����̽���(16ȸ �ݺ�) 
%        > 'Press Z' ������ �߸� zŰ(��� 2) > ... > ��� 15�� ������ �ڵ� ����
% ���� ���������� ���: [result] ����
%     ���������� ���θ�: 1. ID  2. ��Ϲ�ȣ  3. �����ȣ  4. �ü��  5. PC����  6. ȭ�� ��� ��(hz)  
%                   7. �ڵ�: while[1]/������[2] 8. �������: ����[0]/Ű�Է�����[1]/�ݺ���[2]
%                   9. �ڱ� ���ýð�(�ǵ�)  10. �ڱ� ���ӽð�(���α׷�)  11. ����ȭ�� ���ýð�(���α׷�)

%% Clear the workspace and the screen
sca;
close all;
clear all;
clearvars;

%% Configuration settings
% **: Linux �ü�� ��� �� �־�� ��Ȯ���� �������� �ʰų� ������ �Ͼ�� ����.
%     �ּ�ó���� �ڵ�� �׽�Ʈ ���� �� ���� ��������ָ� ��.
%     �Ϻ� ������ �׽�Ʈ ȯ�濡���� ����ȭ�� ���� �� ����.

screenNumber = 0;
islinux = 0;
if islinux == 1
    % PsychLinuxConfiguration # **
    % PsychJavaTrouble(1) **
    Screen('Preference', 'ConserveVRAM', 4096);  % **
    PsychTweak('UseGPUIndex', 1);  % ** PTB-WARNING: Hang in beamposition query detected! ����
    Screen('Preference', 'VBLTimestampingMode', 4);
    Screen('Preference', 'ScreenToHead', 0, 0, 1);
end

% Screen('Preference','Verbosity', 10);  % Sync ��Ȯ���� PTB ���� �������� �������� �ʰ� �˷���.
Screen('Preference','SkipSyncTests', 0);
Screen('Preference','TextRenderer', 1);  % Linux���� 0 >> x11 error

rng('shuffle', 'twister');

%% Test settings
nrepeat = 16;
nblock = 15;
cblock = [1 ceil(nblock/2) nblock];
prompt = {'ID[�ƹ�����]', 'OS[�ƹ�����]', 'PC[�ƹ�����]', 'ȭ�� ��� ��(Hz): ����[60]', '�ڱ� ���ýð�(��): ����[1/60]', '�ڵ�: while[1]/������[2]', '�������: ����[0]/Ű�Է�����[1]/�ݺ���[2]'};
dlgtitle = 'Input';
dims = [1 35];
definput = {'', '', '', '', '', '', ''};
answer = inputdlg(prompt, dlgtitle, dims, definput);

participant = str2double(answer{1, 1});
os = str2double(answer{2, 1});
pc = str2double(answer{3, 1});
hz = str2double(answer{4, 1});
target_t = str2num(answer{5, 1});
whilewhen = str2double(answer{6, 1});
delay = str2double(answer{7, 1});

if delay == 2 && whilewhen == 2
   error('������ �ڵ� & ������� �ݺ��� ������ �Ұ����մϴ�.');
end

mask_t = 2/60;
if delay ~= 1
    blank_t = 6/60;
else
    blank_t = 0;
end

%% Screen settings
% Response keys settings
KbName('UnifyKeyNames');
esc = KbName('ESCAPE');
enter = KbName('Return'); space = KbName('space');
upkey = KbName('UpArrow'); downkey = KbName('DownArrow'); rightkey = KbName('RightArrow'); leftkey = KbName('LeftArrow');
qkey = KbName('q'); okey = KbName('o'); zkey = KbName('z');
key1 = KbName('1!'); key2 = KbName('2@'); key3 = KbName('3#'); key4 = KbName('4$'); key5 = KbName('5%');
key6 = KbName('6^'); key7 = KbName('7&'); key8 = KbName('8*'); key9 = KbName('9('); key0 = KbName('0)');

% color -------------------------------------------------------------------
black = [0 0 0]; white = [255 255 255]; red = [255 0 0];

% ������ ���� --------------------------------------------------------
[win, rect]=Screen('OpenWindow', screenNumber, white, [], [], [], [], 0);
SetMouse(rect(3), rect(4));        % ���콺 Ŀ�� ������+�Ʒ��� ������ �̵�

if islinux == 1
    ListenChar(2); % enable listening, additionally any output of keypresses to Matlabs or Octaves windows is suppressed.
end
% ===========================================================================================

%% Image & text settings
imgloc = round(CenterRectOnPointd([0 0 900 600], rect(3)/2, rect(4)/2));
txtloc_y = imgloc(2)-50;
slack = Screen('GetFlipInterval', win)/2;

mask = imread('stim/900x600_Black.jpg');
mask_tex = Screen('MakeTexture', win, mask);

targetName_g = 'stim/900x600_25_100000_green.jpg';
targetName_r = 'stim/900x600_25_100000_magenta.jpg';
target_g = imread(targetName_g);
target_r = imread(targetName_r);
target_tex_g = Screen('MakeTexture', win, target_g);
target_tex_r = Screen('MakeTexture', win, target_r);

%% Test start
timestamp = [];
for b = 1:nblock
    txtcolor = black;
    txtinst = '--\nPress Z';
    if delay == 2
        targetName = targetName_g;
    else
        target_tex = target_tex_g;
    end

    for c = cblock
        if c == b
            txtcolor = red;
            txtinst = 'CAMERA\nPress Z';
            if delay == 2
                targetName = targetName_r;
            else
                target_tex = target_tex_r;
            end
        end
    end
    DrawFormattedText(win, txtinst, 'center', txtloc_y, txtcolor);
    Screen('Flip', win);
    KbQueueCreate;
    KbQueueStart;
    while true
        [pressed, firstPress, firstRelease, lastPress, lastRelease] = KbQueueCheck; % Collect keyboard events since KbQueueStart was invoked
        if pressed
            if firstPress(esc)
                Screen('Close', win);
            elseif firstPress(zkey)
                break;
            end
        end
    end
    KbQueueStop;
    KbQueueRelease;
    Screen('Flip', win);
    for t = 1:nrepeat
        if whilewhen == 1   % While�� �ڵ�
            txt = strcat('ptb(while)', num2str(hz), '_' , num2str(floor(target_t*1000)), '_', num2str(t));

            % KbPressWait;
            KbQueueCreate;
            KbQueueStart;
            while true
                [pressed, firstPress, firstRelease, lastPress, lastRelease] = KbQueueCheck;
                if pressed
                    if firstPress(esc)
                        Screen('Close', win);
                    elseif firstPress(space)
                        break;
                    end
                end
            end
            KbQueueStop;
            KbQueueRelease;

            blank_onset = GetSecs;
            while GetSecs - blank_onset < blank_t - slack
                Screen('Flip', win);
            end

            target_onset = GetSecs;
            while GetSecs - target_onset < target_t - slack
                if delay == 2
                    target = imread(targetName);
                    target_tex = Screen('MakeTexture', win, target);
                end

                DrawFormattedText(win, txt, 'center', txtloc_y, txtcolor);
                Screen('DrawTexture', win, target_tex, [], imgloc);
                Screen('Flip', win);
            end
            mask_onset = GetSecs;
            while GetSecs - mask_onset < mask_t - slack
                DrawFormattedText(win, txt, 'center', txtloc_y, txtcolor);
                Screen('DrawTexture', win, mask_tex, [], imgloc);
                Screen('Flip', win);
            end
            target_realtime = mask_onset - target_onset;

            mask_offset = GetSecs;
            mask_realtime = mask_offset - mask_onset;
            Screen('Flip',win);
        elseif whilewhen == 2    % ������ �ڵ�
            txt = strcat('ptb(when)', num2str(hz), '_' , num2str(floor(target_t*1000)), '_', num2str(t));

            % KbPressWait;
            KbQueueCreate;
            KbQueueStart;
            while true
                [pressed, firstPress, firstRelease, lastPress, lastRelease] = KbQueueCheck;
                if pressed
                    if firstPress(esc)
                        Screen('Close', win);
                    elseif firstPress(space)
                        break;
                    end
                end
            end
            KbQueueStop;
            KbQueueRelease;

            blank_onset = Screen('Flip', win); % ���� ���� ���۽���

            DrawFormattedText(win, txt, 'center', txtloc_y, txtcolor);
            if delay == 2
                target = imread(targetName);
                target_tex = Screen('MakeTexture', win, target);
            end
            Screen('DrawTexture', win, target_tex, [], imgloc);
            target_onset = Screen('Flip', win, blank_onset + blank_t - slack); % �������� ���۽���

            DrawFormattedText(win, txt, 'center', txtloc_y, txtcolor);
            Screen('DrawTexture', win, mask_tex, [], imgloc);
            mask_onset = Screen('Flip', win, target_onset + target_t - slack);    % �������� ������ = ���� ���۽���
            target_realtime = mask_onset - target_onset;

            mask_offset = Screen('Flip', win, mask_onset + mask_t - slack);     % �������� ������ = ��ȭ�� ���ý���
            mask_realtime = mask_offset - mask_onset;
            Screen('Flip',win);
        end
        timestamp = vertcat(timestamp, [participant b t os pc hz whilewhen delay target_t target_realtime mask_realtime]);
    end
end

if islinux == 1
    ListenChar();
end

Screen('Close', win);

%% Save data file
nowtime = fix(clock);
nowdate_txt = sprintf('%4d%02d%02d_%02d%02d%02d', nowtime(1), nowtime(2), nowtime(3), nowtime(4), nowtime(5), nowtime(6));

fileName0 = strcat('result/matlab', num2str(participant), '_', num2str(os), '_', num2str(pc), '_', num2str(hz), '_', num2str(whilewhen), '_', num2str(delay), '_', num2str(floor(target_t*1000)), '_', nowdate_txt, '.txt');
writetable(table(timestamp), fileName0, 'Delimiter', '\t');
