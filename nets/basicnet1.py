import torch.nn as nn
import torch.nn.functional as F
import math


class basicnet(nn.Module):
    '''
    减少卷基层的层数，采用avepooling
    采用9层结构
    '''

    def __init__(self, features):
        super(basicnet, self).__init__()
        self.features = features
        self.fc = nn.Sequential(
            nn.Dropout(),
            nn.Linear(8*8*64, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Linear(4096, 32),  # hash码位数
        )

        # Initialize weights
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
                m.bias.data.zero_()

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)  # 对齐最高维，即一个batch内的图像数目
        x = self.fc(x)
        x = F.tanh(x)  # 转化到tanh，-1到1之间
        return x


def make_layers(cfg, batch_norm=False):
    layers = []
    in_channels = 3
    for v in cfg:
        if v == 'M':
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        elif v == 'A':
            layers += [nn.AvgPool2d(kernel_size=2, stride=2)]
        else:
            conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1)
            if batch_norm:
                layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
            else:
                layers += [conv2d, nn.ReLU(inplace=True)]
            in_channels = v
    return nn.Sequential(*layers)


cfg = {
    'A': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'B': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'D': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
    'E': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M',
          512, 512, 512, 512, 'M'],
    'x': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M'],
    'y': [32, 'M', 64, 64, 'A'],
}


def makebasicnet():
    return basicnet(make_layers(cfg['y'], batch_norm=True))
